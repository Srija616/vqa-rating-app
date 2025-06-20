import json
import pandas as pd
import argparse
from pathlib import Path

def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

def main(output_file, answer_key_file, qa_master_file, lang_choice, output_csv):
    output_data = {item["ID"]: item["response"] for item in load_jsonl(output_file)}
    answer_data = load_jsonl(answer_key_file)
    qa_data = {item["ID"]: item for item in load_jsonl(qa_master_file)}

    rows = []
    for item in answer_data:
        _id = item["ID"]
        if _id not in output_data or _id not in qa_data:
            continue  # skip if missing response or question

        response = output_data[_id]
        correct = item["correct_nat_val"] if lang_choice == "native" else item["correct_en_val"]
        question = qa_data[_id]["native_question"] if lang_choice == "native" else qa_data[_id]["eng_question"]
        image_path = f"images/Amharic/{_id}.jpg"

        rows.append({
            "id": _id,
            "image_path": image_path,
            "question": question,
            "model_answer": response,
            "correct_answer": correct
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"✅ Saved {len(df)} entries to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file", default="/mnt/data/users/srija/Afri-CVQAv2/inferences/phi/image/text_no_context/output_open_ended.jsonl")
    parser.add_argument("--answer_key_file", default="/mnt/data/users/srija/CVQAv2/CVQAv2/datasets/metadata/answer_keys/et_am.jsonl")
    parser.add_argument("--qa_master_file", default="/mnt/data/users/srija/CVQAv2/CVQAv2/datasets/metadata/qa/master.jsonl")
    parser.add_argument("--lang", choices=["native", "english"], required=True)
    parser.add_argument("--output_csv", default="data_native.csv")
    args = parser.parse_args()

    main(args.output_file, args.answer_key_file, args.qa_master_file, args.lang, args.output_csv)
