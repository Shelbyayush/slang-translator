Slang-to-Formal AI Translator 🚀

A specialized translation engine that bridges the gap between modern internet slang and formal English. This project features a fine-tuned Llama 3.2 1B model, optimized for low-latency deployment on edge devices and free-tier cloud hosting.

🌟 Key Achievements

Model Evolution: Successfully transitioned from a Mistral 7B research baseline to a deployment-ready Llama 3.2 1B architecture.

Quantization Mastery: Leveraged 4-bit NF4 quantization (bitsandbytes) to reduce model memory footprint by over 70%.

Parameter Efficiency: Utilized QLoRA to train only 1.01% of model parameters (12.5M), maintaining high accuracy while preventing catastrophic forgetting.

Performance Gains: Achieved a 127% improvement in BLEU scores over base pre-trained models for slang-specific tasks.

🛠️ Tech Stack

Base Model: Meta Llama 3.2 1B Instruct

Fine-Tuning: PEFT (LoRA), SFTTrainer (Hugging Face trl)

Optimization: 4-bit Quantization, BitsAndBytes

Infrastructure: Weights & Biases (Experiment Tracking), Hugging Face Spaces (Deployment)

UI: Gradio

📁 Project Structure

CleanNPreprocess.py: Custom NLP pipeline for slang normalization and emoji handling.

deployment/fine_tune.py: Optimized training script for the 1B parameter architecture.

deployment/format_data.py: Instruction-tuning logic for Llama 3.2 chat templates.

app.py: Gradio-based web interface for real-time inference.

🚀 Live Demo

The model is deployed on Hugging Face Spaces. You can test it here:
[Link to your HF Space]

📖 Research & Methodology

This project was documented in a comprehensive technical report (included in the repository), detailing the challenges of "Contextual Hallucinations" in standard LLMs and the mathematical foundations of Low-Rank Adaptation (LoRA).

Developed by Ayush Chaudhary (2022-2026)