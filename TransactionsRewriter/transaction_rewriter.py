import sys
import csv


def extract_tokens(s):
    extracted_tokens = set(())
    parts = s.split('+')
    for token in parts:
        amount_and_name = token.split()
        if len(amount_and_name) == 4:
            extracted_tokens.add(amount_and_name[1])
            extracted_tokens.add(amount_and_name[3])
        elif len(amount_and_name) == 2:
            extracted_tokens.add(amount_and_name[1])
        elif len(amount_and_name) == 3:
            extracted_tokens.add(amount_and_name[1] + ' ' + amount_and_name[2])
    return extracted_tokens


def extract_values(s):
    values = {}
    parts = s.split('+')
    for token in parts:
        amount_and_name = token.split()
        if len(amount_and_name) == 4:
            values[amount_and_name[1]] = amount_and_name[0].replace(',', '')
            values[amount_and_name[3]] = amount_and_name[2].replace(',', '')
        elif len(amount_and_name) == 2:
            values[amount_and_name[1]] = amount_and_name[0].replace(',', '')
        elif len(amount_and_name) == 3:
            token_name = amount_and_name[1] + ' ' + amount_and_name[2]
            values[token_name] = amount_and_name[0].replace(',', '')
    return values


def extract_all_tokens(csv_file_name):
    all_tokens = set(())
    with open(csv_file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for r in csv_reader:
            all_tokens.update(extract_tokens(r['Value_IN(Token)']))
            all_tokens.update(extract_tokens(r['Value_OUT(Token)']))
    return all_tokens


def extract_all_rows(csv_file_name):
    all_rows = []
    with open(csv_file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            all_rows.append(row)
    return all_rows


if len(sys.argv) != 2:
    print("Please provide the file path as command argument")
else:
    field_names = ['Txhash', 'Blockno', 'DateTime', 'From', 'To',
                   'Historical $Price/Eth', 'Status', 'ErrCode', 'Method',
                   'Value_IN(ETH)', 'Value_OUT(ETH)', 'TxnFee(ETH)',
                   'Balance(ETH)']
    tokens = extract_all_tokens(sys.argv[1])
    for token in tokens:
        field_names.append('Value_IN({})'.format(token))
        field_names.append('Value_OUT({})'.format(token))
        field_names.append('Balance({})'.format(token))
    rows = extract_all_rows(sys.argv[1])
    with open('transactions_rewritten.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        balances = {'ETH': 0}
        for token in tokens:
            balances[token] = 0
        for row in rows:
            values_in = extract_values(row['Value_IN(Token)'])
            for t in extract_tokens(row['Value_IN(Token)']):
                row['Value_IN({})'.format(t)] = values_in[t]
            values_out = extract_values(row['Value_OUT(Token)'])
            for t in extract_tokens(row['Value_OUT(Token)']):
                row['Value_OUT({})'.format(t)] = values_out[t]
            for token in tokens:
                if 'Value_IN({})'.format(token) not in row:
                    row['Value_IN({})'.format(token)] = 0
                if 'Value_OUT({})'.format(token) not in row:
                    row['Value_OUT({})'.format(token)] = 0
            eth_in = float(row['Value_IN(ETH)'])
            eth_out = float(row['Value_OUT(ETH)'])
            tx_fee = float(row['TxnFee(ETH)'])
            row['Balance(ETH)'] = balances['ETH'] + eth_in - eth_out - tx_fee
            balances['ETH'] = row['Balance(ETH)']
            for token in tokens:
                token_in = float(row['Value_IN({})'.format(token)])
                token_out = float(row['Value_OUT({})'.format(token)])
                token_key = 'Balance({})'.format(token)
                row[token_key] = balances[token] + token_in - token_out
                # handling precision error
                if row[token_key] < 1e-10:
                    row[token_key] = 0
                balances[token] = row['Balance({})'.format(token)]
            row.pop('Value_IN(Token)')
            row.pop('Value_OUT(Token)')
            writer.writerow(row)







