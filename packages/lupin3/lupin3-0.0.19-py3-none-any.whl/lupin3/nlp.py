#
#
# # try:
# #
# #     from transformers import BertConfig
# #     from transformers import BertTokenizer, BertModel
# #
# # except ImportError:
# #     print("gevent library not found - installing...")
# #     autoinstall.install_package("transformers==4.23.1")
#
#
# from transformers import BertConfig
# from transformers import BertTokenizer, BertModel
#
# model_name = 'uer/sbert-base-chinese-nli'
# config = BertConfig.from_pretrained(model_name)
# tokenizer = BertTokenizer.from_pretrained(model_name)
# model = BertModel.from_pretrained(model_name)
#
# from sklearn.metrics.pairwise import cosine_similarity
# import torch
#
#
# def getsim(targetitem, alllist, MAX_LENGTH=5, TRUNCATION=True):
#     savenum = 3
#     sentences = []
#     sentences.append(targetitem)
#     sentences += alllist
#     #     sentences = [
#     #        '米酒', '米酒味','路易波士茶'
#     #     ]
#     #     # for word in
#
#     tokens = {'input_ids': [], 'attention_mask': []}
#
#     for sentence in sentences:
#         new_tokens = tokenizer.encode_plus(sentence, max_length=MAX_LENGTH, truncation=TRUNCATION, padding='max_length',
#                                            return_tensors='pt')
#         tokens['input_ids'].append(new_tokens['input_ids'][0])
#         tokens['attention_mask'].append(new_tokens['attention_mask'][0])
#
#     tokens['input_ids'] = torch.stack(tokens['input_ids'])
#     tokens['attention_mask'] = torch.stack(tokens['attention_mask'])
#     outputs = model(**tokens)
#     embeddings = outputs.last_hidden_state
#     attention_mask = tokens['attention_mask']
#     mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
#     masked_embeddings = embeddings * mask
#     summed = torch.sum(masked_embeddings, 1)
#     summed_mask = torch.clamp(mask.sum(1), min=1e-9)
#     mean_pooled = summed / summed_mask
#     mean_pooled = mean_pooled.detach().numpy()
#     result = cosine_similarity([mean_pooled[0]], mean_pooled[1:])
#
#     return result