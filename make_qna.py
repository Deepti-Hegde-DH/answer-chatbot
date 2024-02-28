from transformers import GPTNeoForCausalLM, GPT2Tokenizer

class QuestionGenerator:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.questions = []
        self.answers = []

    def _generate_questions_and_answers(self, input_text):
        # Load pre-trained GPT-Neo model and tokenizer
        model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-2.7B")
        tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B")

        # Tokenize the input text
        input_ids = tokenizer.encode(input_text, return_tensors="pt")

        # Generate questions and answers using the model
        for i in range(5):  # You can adjust the number of questions generated
            output = model.generate(input_ids, max_length=100, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95)
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
            question, answer = generated_text.split('? ')
            self.questions.append(question.strip())
            self.answers.append(answer.strip())

    def generate_questions(self):
        with open(self.input_file_path, 'r') as file:
            input_text = file.read()
        chunk_size = 4096
        chunks = [input_text[i:i+chunk_size] for i in range(0, len(input_text), chunk_size)]
        for chunk in chunks:
            self._generate_questions_and_answers(chunk)
        with open('questions/'+ self.input_file_path.split('/')[-1], 'w') as file:
            for i, question in enumerate(self.questions, 1):
                file.write(f"{i}. {question}\n")
        with open('answers/'+ self.input_file_path.split('/')[-1], 'w') as file:
            for i, (question, answer) in enumerate(zip(self.questions, self.answers), 1):
                file.write(f"{i}. Question: {question}\n   Answer: {answer}\n\n")

