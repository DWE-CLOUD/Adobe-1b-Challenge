from sentence_transformers import SentenceTransformer
import os

print("Downloading and saving the sentence transformer model...")
model_name = 'sentence-transformers/multi-qa-MiniLM-L6-cos-v1'
save_path = os.path.join('models', model_name.split('/')[-1]) # Cleaner path
os.makedirs(save_path, exist_ok=True)
model = SentenceTransformer(model_name)
model.save(save_path)
print(f"Model saved successfully to '{save_path}'")