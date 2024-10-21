
def find_embed_lines(readme_path, lookup_string):
    embed_lines = []
    
    with open(readme_path, 'r') as file:
        for line in file:
            if lookup_string in line:
                embed_lines.append(line.strip())
    
    return embed_lines

def read_embeds_from_readme(embed_lines, lookup_string):
    embed_dict = {}

    for embed_line in embed_lines:
        script_path_str = embed_line.split(lookup_string)[-1].strip()
        script_path = script_path_str
        try:
            # Read the script content as a string
            with open(script_path, 'r') as script_file:
                script_content = script_file.read()

            # Store the content in the dictionary with the file path as the key
            embed_dict[script_path_str] = script_content

        except FileNotFoundError:
            print(f"Error: {script_path} not found.")

    return embed_dict

def replace_embeds_in_readme(readme_path, embed_dict, lookup_string):
    # Read the README.md content
    with open(readme_path, 'r') as readme_file:
        readme_content = readme_file.readlines()

    updated_lines = []
    inside_replacement_script = False
    # Loop through each line in the README.md
    for line in readme_content:
        if line.startswith(lookup_string):
            updated_lines.append(line)
            inside_replacement_script = True
            embed_tag = line.strip()
            embed_path = embed_tag.split(lookup_string)[1]
            # If the embed_path is in our dictionary, insert the script code after the embed tag
            if embed_path in embed_dict:
                script_content = embed_dict[embed_path]
                # Add the script content as a code block after the embed tag
                updated_lines.append(f"{script_content}")
        elif line.startswith('```') & inside_replacement_script:
            updated_lines.append('\n')
            updated_lines.append(line)
            inside_replacement_script = False 
        elif not inside_replacement_script:
            updated_lines.append(line)
        

    # Write the updated content back to README.md
    with open(readme_path, 'w') as readme_file:
        readme_file.writelines(updated_lines)

    print("README.md updated successfully.")
