import pandas as pd

files = {
    "processed/ngoai_ngu_2021.csv": "Yêu cầu về Ngoại Ngữ 2021",
    "processed/ngoai_ngu_2024.csv": "Yêu cầu về Ngoại Ngữ 2024",
    "processed/quy_che_2018.csv": "Quy chế từ 2018",
    "processed/quy_che_2023.csv": "Quy chế từ 2023"
}

merged_dataframes = []

for path, origin in files.items():
    df = pd.read_csv(path)
    df['from'] = origin
    merged_dataframes.append(df)

merged_df = pd.concat(merged_dataframes, ignore_index=True)

merged_df = merged_df[['id', 'from', 'chapter', 'section', 'content']]

output_path = "final.csv"
merged_df.to_csv(output_path, index=False, quoting=1)
