import markovify

# Get raw text as string.
with open("C:/Users/Owner/Desktop/5303-DB-Matamoros/A9/1.txt", errors ="ignore") as f:
    text_a = f.read()

with open("C:/Users/Owner/Desktop/5303-DB-Matamoros/A9/2.txt", errors="ignore") as g:
    text_b = g.read()

# Build the models
model_a = markovify.Text(text_a)
model_b = markovify.Text(text_b)
print(type(model_a))
# Combine the models. The numbers indicate how much weight to give a particular model
model_combo = markovify.combine([ model_a, model_b ], [ 1, 1.5 ])
print(type(model_combo))

# # Print five randomly-generated sentences
# for i in range(5):
#     print(model_combo.make_sentence())

# print ("\n")

# # Print three randomly-generated sentences of no more than 280 characters
# for i in range(3):
#     print(model_combo.make_short_sentence(280))