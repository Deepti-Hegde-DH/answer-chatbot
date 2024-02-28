#========================================
import os 
from crop import crop_pdf

#*****
#cropping the pdf file to remove headers and footers.
#*****

input_pdf_path = "unprocessed_files/"
output_pdf_path = "cropped_files/"

file_list = [f for f in os.listdir(input_pdf_path) if os.path.isfile(os.path.join(input_pdf_path, f))]

for i in file_list:
    top_margin = 5
    bottom_margin = 10
    left_margin = 5

    crop_pdf(input_pdf_path+i, output_pdf_path, top_margin, bottom_margin, left_margin)
#======================================================
from get_text import clean_text

#*****
#removing all gibberish /irrelevant content
#*****

file_list = [f for f in os.listdir(output_pdf_path) if os.path.isfile(os.path.join(output_pdf_path, f))]
processed_path = 'Processed_files/'
for i in file_list:
    clean_text(output_pdf_path+i,processed_path)
#=======================================================

#
#*****
#generating the questions file answer key file
#*****
file_list = [f for f in os.listdir(processed_path) if os.path.isfile(os.path.join(processed_path,f))]
for i in file_list:
    with open(processed_path+i, 'r')as txt:
        content = txt.read()
        content = " ".join(content.split())
        text_tokens = content.split()
        sentences = []
        window_size=80
        for i in range(0, len(text_tokens), 15):
            window = text_tokens[i : i + window_size]
        if len(window) < window_size:
            break
        sentences.append(window)
        paragraphs = [" ".join(s) for s in sentences]
        model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        model.max_seq_length = 512
        cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        embeddings = model.encode(
        paragraphs,
        show_progress_bar=True,
        convert_to_tensor=True,
    )
        query = "what is cloud computing?"
        query_embeddings = model.encode(query, convert_to_tensor=True)
        query_embeddings = query_embeddings.cuda()
        hits = util.semantic_search(
            query_embeddings,
            embeddings,
            top_k=top_k,
        )[0]

        cross_input = [[query, paragraphs[hit["corpus_id"]]] for hit in hits]
        cross_scores = cross_encoder.predict(cross_input)

        for idx in range(len(cross_scores)):
            hits[idx]["cross_score"] = cross_scores[idx]

        results = []
        hits = sorted(hits, key=lambda x: x["cross_score"], reverse=True)
        for hit in hits[:5]:
            results.append(paragraphs[hit["corpus_id"]].replace("\n", " "))
        print(results)
