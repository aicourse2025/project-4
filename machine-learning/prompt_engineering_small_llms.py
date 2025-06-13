"""
    Prompt engineering of small LLMs
"""

import pandas as pd
from transformers import (
    T5Tokenizer,
    T5ForConditionalGeneration,
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Trainer,
    EncoderDecoderModel,
    TrainingArguments
)

# Load model and tokenizer
MODEL_NAME = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

# Define a function to summarize a chunk of text
def summarize_text(text, max_input_length=512, max_output_length=150):
    """
    Generates a concise summary of the input text using a T5 language model.

    Args:
        text (str): The input text to be summarized.
        max_input_length (int, optional): Maximum length of the input text in tokens. 
            Defaults to 512.
        max_output_length (int, optional): Maximum length of the generated summary in tokens. 
            Defaults to 150.

    Returns:
        str: A generated summary of the input text.

    Note:
        The function uses a T5 model with beam search (num_beams=4) and length penalty
        to generate high-quality summaries. The input text is prefixed with "summarize: "
        to indicate the summarization task to the model.
    """
    input_text = f"summarize: {text.strip()}"
    inputs = tokenizer.encode(
        input_text, return_tensors="pt", max_length=max_input_length, truncation=True
    )
    summary_ids = model.generate(
        inputs,
        max_length=max_output_length,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

df = pd.read_csv("/top3_products.csv")
df["prompt"] = df["positive_reviews"].fillna("") + "\n" + df["negative_reviews"].fillna("")

grouped = df.groupby("name")

# Loop through each category
for category, group in grouped:
    REVIEWS = " ".join(group["prompt"].astype(str).tolist())
    summary = summarize_text(REVIEWS)

    print(f"\n=== Summary for Category: {category} ===\n")
    print(summary)


# 1. Setup model and tokenizer
MODEL_NAME = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# 2. Few-shot examples for style guidance
few_shot_examples = [
    {
        "role": (
            "You are an top reviewer for products.You write in complete sentences "
            "and high level english like the bloggers from WireCutter and."),
        "input": ("Review:\nGreat vacuum: strong suction, quiet operation, "
                  "but battery life is short.\n\nBlog-style review:"),
        "output": ("This vacuum excels with its powerful suction and whisper-quiet "
                   "performance. However, its battery life is on the shorter side, "
                   "so if you need extended runtime, keep a charger nearby.")
    },
    {
        "role": ("You are an top reviewer for products. You write in complete sentences "
                 "and high level english like the bloggers from WireCutter and."),
        "input": ("Review:\nSmart speaker with rich audio, sometimes mishears "
                  "commands. Good value.\n\nBlog-style review:"),
        "output": ("Delivering impressive sound quality at an affordable price, "
                   "this smart speaker is a solid choice—although occasional "
                   "voice recognition hiccups can be a minor annoyance.")
    }
]

# 3. Helper to build few-shot prompt
def build_prompt(examples, new_review):
    """
    Builds a prompt string by combining few-shot examples with a new review.
    
    Args:
        examples (list): List of dictionaries containing example prompts and their outputs.
            Each dictionary should have 'role', 'input', and 'output' keys.
        new_review (str): The new review text to be processed.
        
    Returns:
        str: A formatted prompt string that combines the examples and the new review.
    """

    prompt_str = ""
    for ex in examples:
        prompt_str += f"{ex['role']}\n{ex['input']}\n{ex['output']}\n\n"
    prompt_str += f"Review:\n{new_review}\n\nBlog-style review:"
    return prompt_str

# 4. Load your dataset and combine reviews
df = pd.read_csv("/content/top3_products.csv")
df["prompt"] = df["positive_reviews"].fillna("") + "\n" + df["negative_reviews"].fillna("")

# 5. Run summarization per product
for product_name, group in df.groupby("name"):
    COMBINED_REVIEW = " ".join(group["prompt"].drop_duplicates().astype(str).tolist())
    prompt_text = build_prompt(few_shot_examples, COMBINED_REVIEW)

    inputs_t = tokenizer(prompt_text, return_tensors="pt", truncation=True, max_length=1024)
    outputs = model.generate(
        **inputs_t,
        max_new_tokens=600,
        num_beams=4,
        length_penalty=1.2,
        early_stopping=True
    )
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(f"\n=== {product_name} ===\n{summary}\n")

# 1. Setup model and tokenizer
MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# 2. Few-shot examples for style guidance

few_shot_examples = [
    {
        "role": "You are a professional product reviewer writing a concise blog post to help customers choose the best product. Use full sentences and correct english. Do not repeat yourself. Write in the third person about the product", "example": "There are no bad iPads. That’s the best news about Apple’s tablet lineup: 15 years after Steve Jobs first debuted the device, the iPad is the best tablet on the market, and it’s not particularly close. Apple’s App Store is enormous and filled with great apps, Apple’s performance and battery life are consistently excellent, and the iPad is still the company’s most versatile device. That’s one easy answer to your question: yes, if you want a tablet you should buy an iPad. Even last year’s iPad, or heck, last-last year’s iPad is still a solid device. Buying an older but better device — last year’s Pro instead of this year’s Air, for instance — is a tried and true iPad formula. The simplest way to pick an iPad is by process of elimination. First, there’s your budget: you can spend $350 on an iPad, you can spend $2,728 on an iPad, or you can spend just about anything in between. You should also decide whether you need an Apple Pencil and which one has the features you need, because not every iPad supports every model. The same goes for the keyboard attachments. Between price and accessories, your choice might be instantly obvious."
    },
    {
        "role": "You are a professional product reviewer writing a concise blog post to help customers choose the best product. Use full sentences and correct english. Do not repeat yourself. Write in the third person about the product","example": "Today’s robot vacuums are becoming a bit like cars: with all the features, upgrades, and fancy trimmings available these days, it’s easy to forget that they can just be simple machines that get us from point A to point B. Yes, some bots blow hot air on their bums (mop pads), deftly navigate dog poop, and have arms to pick up your socks, but there are plenty of basic budget robot vacuums that just do a decent job of cleaning your floor autonomously — as long as you tidy up first. Fancier models have obstacle recognition, and some even use AI-powered cameras to tell popcorn from poop and avoid the latter. If you want one of those, check out my best robot vacuum buying guide. But if you think you can manage the task of picking up after yourself (and your puppy), a budget bot will save you a lot of money and still do a good job cleaning your floor."
    },
    {
        "role": "You are a professional product reviewer writing a concise blog post to help customers choose the best product. Use full sentences and correct english. Do not repeat yourself. Write in the third person about the product","example": "So, you’re thinking of buying a smart ring. Well, some good news. Picking the best of the lot is incredibly easy right now. The “bad” news is that, as far as trustworthiness and reliability, your choices are somewhat limited, as this is still a niche and emerging gadget category. Smart rings are in the middle of a resurgence. That means a lot of experimental ideas and newcomer tech brands you’ve probably never heard of. Enough competitors have cropped up that I spent the better part of last summer rocking six rings like a high-tech mafia don. While these aren’t necessarily bad products (some are pretty good), many aren’t as polished as what you’d see in more mature categories like smartwatches, headphones, and smartphones. Speaking of which, there are a few things to know about the category. Currently, these devices are primarily health trackers. Their benefit is they’re more discreet and are better suited to sleep tracking than a smartwatch. However, the vast majority don’t include smart alarms or push notifications. This makes them best suited to casual athletes or more wellness-minded people. Hardcore athletes would be better served in most cases by a smartwatch or fitness tracker, with a smart ring as a supplementary source of data. (But that’s quite an expensive endeavor.) Smart rings are also ill-suited for weightlifters, as they can easily scratch against equipment. With that in mind, here’s the best smart ring for most people in 2025 — and a handful of runners-up worth highlighting for the more tech-adventurous."
    }
]

# 3. Helper to build few-shot prompt
def build_add_prompt(examples, new_review):
    """
    Builds a prompt string by combining few-shot examples with a new review.
    
    Args:
        examples (list): List of dictionaries containing example prompts and their outputs.
            Each dictionary should have 'role', 'input', and 'output' keys.
        new_review (str): The new review text to be processed.
        
    Returns:
        str: A formatted prompt string that combines the examples and the new review.
    """

    prompt_str = ""
    for ex in examples:
        prompt_str += f"{ex['role']}\n{ex['example']}\n\n"
    prompt_str += f"Review:\n{new_review}\n\nBlog-style review:"
    return prompt_str

# 4. Load your dataset and combine reviews
df = pd.read_csv("/content/top3_products.csv")
print(df.head)
df["prompt"] = df["positive_reviews"].fillna("") + "\n" + df["negative_reviews"].fillna("")

# 5. Run summarization per product
for product_name, group in df.groupby("name"):
    COMBINED_REVIEW = " ".join(group["prompt"].drop_duplicates().astype(str).tolist())
    prompt_text = build_add_prompt(few_shot_examples, COMBINED_REVIEW)

    inputs_token = tokenizer(prompt_text, return_tensors="pt", truncation=True, max_length=1024)
    outputs = model.generate(
        **inputs_token,
        max_new_tokens=1000,
        num_beams=4,
        length_penalty=1.2,
        early_stopping=True
    )
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(f"\n=== {product_name} ===\n{summary}\n")

# 1. Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")

# 2. Build Encoder-Decoder
model = EncoderDecoderModel.from_encoder_decoder_pretrained(
    "xlm-roberta-base",  # encoder
    "facebook/bart-base"  # decoder (autoregressive, supports generation)
)

# Load dataset
dataset = pd.read_csv("/content/top3_products.csv")
dataset["prompt"] = (
    dataset["positive_reviews"].fillna("") + "\n" + dataset["negative_reviews"].fillna("")
)


# Tokenize the dataset
def tokenize_function(examples):
    """
    Tokenizes input text and target summaries for text summarization model training.
    
    Args:
        examples (dict): Dictionary containing 'source_text' and 'target_summary' keys
            - source_text (str): The input text to be summarized
            - target_summary (str): The target summary text
            
    Returns:
        dict: Dictionary containing tokenized inputs and labels
            - input_ids: Tokenized input text
            - attention_mask: Attention mask for input text
            - labels: Tokenized target summary
    """

    model_inputs = tokenizer(examples["source_text"], max_length=1024, truncation=True)
    labels = tokenizer(examples["target_summary"], max_length=128, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = dataset.map(tokenize_function, batched=True)


# set-up training arguements
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
)


#initialize the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer,
)

trainer.train()

# Tokenize & summarize
SEQUENCE = "Long product reviews ..."
inputs_tokenizer = tokenizer(
    SEQUENCE,
    return_tensors="pt",
    truncation=True,
    padding="max_length",
    max_length=512
)

# 4. Generate
outputs = model.generate(
    input_ids=inputs_tokenizer["input_ids"],
    attention_mask=inputs_tokenizer["attention_mask"],
    max_new_tokens=150,
    num_beams=4,
    length_penalty=1.2,
)

summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
