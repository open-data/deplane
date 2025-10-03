def read_docx(document):
    """
    :param document: docx document object
    """
    dep_fields = []

    dep_comments = []
    for paragraph in document.paragraphs:
        if not paragraph.text.startswith('1-') and not paragraph.text.startswith('2-') and not paragraph.text.startswith('3-'):
            continue
        dep_comments.append('\nDEP: ' + paragraph.text.strip())

    heading_index = 0
    for index, table in enumerate(document.tables):

        if index in [0, 1]:
            continue  # skip reference tables

        dep_field = {}
        is_options_table = False
        iter_jump = 0
        iter_max = 1
        iter_indx = ''

        for row_index, row in enumerate(table.rows):

            if row_index == 0:
                # check to see if the table is a controlled list table
                if row.cells[0].text.strip() == 'Code':
                    is_options_table = True
                    iter_max = 2
                if row.cells[0].text.strip() == 'Attribute':
                    dep_field['YAML_COMMENTS'] = dep_comments[heading_index]
                    heading_index += 1
                continue  # skip table headers

            for cell in row.cells:
                if iter_jump > iter_max:
                    iter_jump = 0
                    iter_indx = ''
                if iter_jump == 0:
                    iter_indx = cell.text.strip()
                    iter_jump += 1
                    continue
                if is_options_table and iter_indx not in dep_field:
                    dep_field[iter_indx] = {'en': '', 'fr': ''}
                if iter_jump == 1:
                    if is_options_table:
                        dep_field[iter_indx]['en'] = cell.text.strip()
                    else:
                        dep_field[iter_indx] = cell.text.strip()
                    iter_jump += 1
                    continue
                if iter_jump == 2:
                    if is_options_table:
                        dep_field[iter_indx]['fr'] = cell.text.strip()
                    else:
                        dep_field[iter_indx] = cell.text.strip()
                    iter_jump += 1
                    continue

        dep_fields.append(dep_field)

    # FIXME: we assume that the 2 resources would not share the same datastore_ids
    #        in most cases they do, like month and year, or service_id, etc.
    #        we have to figure out how to differenciate between Resource 1 and
    #        Resource 2 etc etc from the DEP

    dep_data_dict = {}
    for index, dep_field in enumerate(dep_fields):
        if 'ID' not in dep_field:
            # this is a choices dict, add to previous field
            dep_data_dict[dep_fields[index-1]['ID']]['choices'] = dep_field
            continue
        if dep_field['ID'] not in dep_data_dict:
            dep_data_dict[dep_field['ID']] = {}
        if 'YAML_COMMENTS' in dep_field:
            dep_data_dict[dep_field['ID']] = {'YAML_COMMENTS': dep_field['YAML_COMMENTS']}
        # TODO: handle example values
        if dep_field.get('Field Name EN') and dep_field.get('Field Name FR'):
            dep_data_dict[dep_field['ID']]['label'] = {
                'en': dep_field['Field Name EN'],
                'fr': dep_field['Field Name FR'],
            }
        if dep_field.get('Description EN') and dep_field.get('Description FR'):
            dep_data_dict[dep_field['ID']]['description'] = {
                'en': dep_field['Description EN'],
                'fr': dep_field['Description FR'],
            }
        if dep_field.get('Obligation EN') and dep_field.get('Obligation FR'):
            dep_data_dict[dep_field['ID']]['obligation'] = {
                'en': dep_field['Obligation EN'],
                'fr': dep_field['Obligation FR'],
            }
        if dep_field.get('Occurrence'):
            dep_data_dict[dep_field['ID']]['occurrence'] = dep_field['Occurrence']
        if dep_field.get('Validation EN') and dep_field.get('Validation FR'):
            dep_data_dict[dep_field['ID']]['validation'] = {
                'en': dep_field['Validation EN'],
                'fr': dep_field['Validation FR'],
            }
        if dep_field.get('Character Limit'):
            dep_data_dict[dep_field['ID']]['max_chars'] = dep_field['Character Limit']
    return dep_data_dict