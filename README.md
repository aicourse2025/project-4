# project-4


# Small LLM Prompt-engineering

The small prompt engineering notebook consists of various attempts to prompt-engineer smaller LLMs that are already uniquely designed to produce summaries.

## Small LLMs
- T5-small
- Flan-T5-base
- Flan-T5-large

This project utilizes the FLAN-T5-base and FLAN-T5-base, as well as the T5-small model from the Hugging Face transformers library to generate high-quality, blog-style product reviews from raw product review data. The model is guided by few-shot examples to produce polished summaries that resemble the writing style of top product reviewers.

## Description
The code demonstrates the following steps:
 - Loading the FLAN-T5-base/large or T5-small model and tokenizer from Hugging Face.
 - Using few-shot examples to guide the model in generating blog-style reviews.
 - Loading a product review dataset from a CSV file.
 - Combining positive and negative reviews for each product.
 - Generating a summary using the model for each product, styled like a professional review (similar to Wirecutter blog style).
 - Printing the output summary for each product.

## Findings:
After different attempts at prompting and variation in the model configuration the summary output from the models was strongly effected by the tokenized, broken English of the data set, and often returned summaries in similarly broken English or sentence fragments, often displaying repetition and speaking from the first person (a reflection of whom ever wrote the review in the original data). Likewise, these small models could not be trained to adopt a role in product review expertise that would reflect a more professional tone in the output. It seems that these LLMs are best applied to this kind of task with very short and concise general analysis of a product.
