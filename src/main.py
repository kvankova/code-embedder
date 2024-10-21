from src import job

readme_path = 'README.md'
print("README path: ", readme_path)
lookup_string = "```python:"

if __name__ == '__main__':
    script_to_embed = job.find_embed_lines(
        readme_path = readme_path, 
        lookup_string = lookup_string
        )
    
    print(script_to_embed)

    embed_dict = job.read_embeds_from_readme(
        embed_lines=script_to_embed, 
        lookup_string = lookup_string
        )

    job.replace_embeds_in_readme(
        readme_path = readme_path, 
        embed_dict = embed_dict, 
        lookup_string = lookup_string
        )