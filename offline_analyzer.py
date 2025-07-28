import fitz
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer, util
import nltk
import time
import glob
import json
import os
import hashlib
import argparse

nltk.data.path.append('./nltk_data')

class FastDocumentAnalyst:
    def __init__(self,
                 bi_encoder_model='models/multi-qa-MiniLM-L6-cos-v1',
                 cache_dir='cache_fast',
                 silent=False):
        self.silent = silent
        if not self.silent:
            print(f"Initializing lightweight models from local path: '{bi_encoder_model}'...")
        self.bi_encoder = SentenceTransformer(bi_encoder_model)
        self.cross_encoder = None
        self.cache_dir = cache_dir
        self.index = None
        self.chunk_map = []
        os.makedirs(self.cache_dir, exist_ok=True)
        if not self.silent:
            print("Models initialized.")

    def _get_cache_key(self, pdf_paths: list) -> str:
        file_info = "".join(sorted([f"{path}{os.path.getmtime(path)}" for path in pdf_paths]))
        return hashlib.md5(file_info.encode()).hexdigest()

    def _smart_chunker(self, text: str, chunk_size: int = 256, overlap: int = 50) -> list[str]:
        if not text.strip():
            return []
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk_words = []
        for sentence in sentences:
            sentence_words = sentence.split()
            if len(current_chunk_words) + len(sentence_words) > chunk_size and current_chunk_words:
                chunks.append(" ".join(current_chunk_words))
                current_chunk_words = current_chunk_words[-overlap:]
            current_chunk_words.extend(sentence_words)
        if current_chunk_words:
            chunks.append(" ".join(current_chunk_words))
        return chunks

    def build_or_load_index(self, pdf_paths: list):
        cache_key = self._get_cache_key(pdf_paths)
        index_path = os.path.join(self.cache_dir, f"{cache_key}.index")
        map_path = os.path.join(self.cache_dir, f"{cache_key}.json")

        if os.path.exists(index_path) and os.path.exists(map_path):
            if not self.silent:
                print(f"Loading cached index '{cache_key}'...")
            self.index = faiss.read_index(index_path)
            with open(map_path, 'r', encoding='utf-8') as f:
                self.chunk_map = json.load(f)
            if not self.silent:
                print("Cache loaded successfully.")
            return

        if not self.silent:
            print("No valid cache found. Building new index...")

        all_doc_chunks = []
        for path in pdf_paths:
            if not self.silent:
                print(f"Processing document: {os.path.basename(path)}")
            try:
                with fitz.open(path) as doc:
                    doc_name = os.path.basename(path)
                    for page_num, page in enumerate(doc):
                        text = page.get_text("text")
                        if not text.strip(): continue
                        chunks = self._smart_chunker(text)
                        for chunk in chunks:
                            all_doc_chunks.append({
                                "document": doc_name,
                                "page": page_num + 1,
                                "text": chunk
                            })
            except Exception as e:
                if not self.silent: print(f"Error processing {path}: {e}")

        self.chunk_map = all_doc_chunks
        all_chunks_text = [chunk['text'] for chunk in self.chunk_map]

        if not all_chunks_text:
            if not self.silent: print("No text could be extracted from the documents. Aborting.")
            return

        if not self.silent: print(f"Encoding {len(all_chunks_text)} text chunks...")
        embeddings = self.bi_encoder.encode(
            all_chunks_text,
            show_progress_bar=not self.silent,
            convert_to_numpy=True
        )
        faiss.normalize_L2(embeddings)

        embedding_dim = embeddings.shape[1]
        num_embeddings = embeddings.shape[0]

        PQ_TRAINING_THRESHOLD = 256

        if num_embeddings < PQ_TRAINING_THRESHOLD:
            if not self.silent:
                print(
                    f"Dataset is small ({num_embeddings} vectors). Using a simpler, exact search index (IndexFlatIP).")
            self.index = faiss.IndexFlatIP(embedding_dim)
        else:
            if not self.silent:
                print(
                    f"Dataset is large enough ({num_embeddings} vectors). Using a fast, approximate index (IndexIVFPQ).")
            nlist = max(4, min(100, num_embeddings // 40))
            quantizer = faiss.IndexFlatIP(embedding_dim)
            self.index = faiss.IndexIVFPQ(quantizer, embedding_dim, nlist, 8, 8)
            if not self.silent:
                print("Training the approximate index...")
            self.index.train(embeddings)
        
        self.index.add(embeddings)

        if not self.silent: print("Saving index to cache...")
        faiss.write_index(self.index, index_path)
        with open(map_path, 'w', encoding='utf-8') as f:
            json.dump(self.chunk_map, f)
        if not self.silent: print("Index built and saved.")

    def search_and_retrieve(self, query_embedding, top_k: int = 30) -> list:
        if not self.index:
            raise RuntimeError("Index is not built. Please call `build_or_load_index` first.")

        if not self.silent: print("Step 1: Fast Retrieval...")

        if hasattr(self.index, 'nprobe'):
            self.index.nprobe = 10

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1:
                chunk = self.chunk_map[idx]
                chunk['score'] = float(dist)
                results.append(chunk)

        return results

    def _create_local_synthesis(self, query_embedding, context_chunks: list, num_takeaways: int = 25) -> dict:
        if not self.silent:
            print("Step 2: Generating Local Extractive Synthesis...")

        all_sentences = []
        sentence_map = []
        for chunk in context_chunks:
            sentences = nltk.sent_tokenize(chunk['text'])
            for sentence in sentences:
                all_sentences.append(sentence)
                sentence_map.append(f"(Source: {chunk['document']}, Page: {chunk['page']})")

        if not all_sentences:
            return {"takeaways": []}

        sentence_embeddings = self.bi_encoder.encode(
            all_sentences, show_progress_bar=not self.silent, convert_to_numpy=True
        )
        similarities = util.cos_sim(query_embedding, sentence_embeddings)[0]

        top_indices = np.argsort(-similarities.cpu().numpy())

        key_takeaways = []
        seen_sentences = set()
        for idx in top_indices:
            if len(key_takeaways) >= num_takeaways: break
            sentence_text = all_sentences[idx].strip()
            if sentence_text and sentence_text not in seen_sentences:
                key_takeaways.append({"text": sentence_text, "source": sentence_map[idx]})
                seen_sentences.add(sentence_text)

        return {"takeaways": key_takeaways}

    def run_analysis(self, pdf_paths: list, persona: str, job_to_be_done: str) -> dict:
        start_time = time.time()
        self.build_or_load_index(pdf_paths)
        if not self.index:
            return {"error": "Index could not be built. No text extracted."}

        query = f"Persona: {persona}. Task: {job_to_be_done}"
        query_embedding = self.bi_encoder.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)

        top_results = self.search_and_retrieve(query_embedding)

        if not top_results:
            return {"error": "No relevant information found for the given query."}

        synthesis_result = self._create_local_synthesis(query_embedding, top_results)

        output = {
            "metadata": {
                "analysis_type": "Fast Extractive Summary",
                "input_documents": [os.path.basename(path) for path in pdf_paths],
                "persona": persona,
                "job_to_be_done": job_to_be_done,
                "processing_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "processing_time_seconds": round(time.time() - start_time, 2)
            },
            "actionable_synthesis": synthesis_result["takeaways"],
            "supporting_evidence": [
                {
                    "rank": i + 1,
                    "document": res['document'],
                    "page": res['page'],
                    "relevance_score": f"{res['score']:.4f}",
                    "text_excerpt": res['text']
                } for i, res in enumerate(top_results)
            ]
        }
        return output


def main():
    parser = argparse.ArgumentParser(description="Fast Document Analyst")
    parser.add_argument('pdf_directory', type=str, help="Directory containing PDF files to analyze.")
    parser.add_argument('-p', '--persona', type=str, required=True,
                        help="Persona for the analysis (e.g., 'A financial analyst').")
    parser.add_argument('-j', '--job', type=str, required=True,
                        help="Job to be Done (e.g., 'Assess Q4 financial risks').")
    parser.add_argument('-o', '--output', type=str, default="fast_analysis_output.json",
                        help="Path to save the output JSON file.")
    parser.add_argument('--json', action='store_true',
                        help="Enable JSON-only output to stdout, suppressing status messages.")

    args = parser.parse_args()

    analyst = FastDocumentAnalyst(silent=args.json)

    if not os.path.isdir(args.pdf_directory):
        print(f"Error: The directory '{args.pdf_directory}' does not exist.")
        return

    pdf_files = glob.glob(os.path.join(args.pdf_directory, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in '{args.pdf_directory}'.")
        return

    if not args.json:
        print(f"Found {len(pdf_files)} PDF(s) to analyze.")

    result = analyst.run_analysis(
        pdf_paths=pdf_files,
        persona=args.persona,
        job_to_be_done=args.job
    )

    if args.json:
        print(json.dumps(result, indent=4))
    else:
        print(f"\nAnalysis complete. Saving output to '{args.output}'...")
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print("\n--- Actionable Synthesis ---")
        synthesis = result.get("actionable_synthesis")
        if synthesis:
            for item in synthesis:
                print(f"- {item['text']} {item['source']}")
        else:
            print(result.get("error", "No summary could be generated."))
        print("--------------------------")


if __name__ == '__main__':
    main()