#Market Basket Analysis #
#2019-05-09             #
#Semih Acikgoz          #

#Import libraries to read, manupulate and analyse data
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#import data to a dataframe
df = pd.read_csv(r"C:\Users\acikgozs\Documents\mba.txt", sep = ";")

#drop lines which does not have an invoice line
#inplace --> keeps the DataFrame with valid entries in the same variable        #
#dropna - axis = 0 => rows, axis = 1 => columns                                 #
df.dropna(axis = 0, subset = ["INVOICEID"], inplace = True)

#Grouping items based on FSC
#unstack; pivots table based on input level. Default level is -1(last level)    #
#In this case invoiceid stays the same, itemid(last level) will be pivoted      #
basket = (df.groupby(["INVOICEID", "ITEMID"])["UNITS"]
        .sum().unstack().reset_index().fillna(0)
        .set_index("INVOICEID")
    )

#matching frequent bought items
frequent_items = apriori(basket, min_support = 0.05, use_colnames = True)

#genrating rules
rules = association_rules(frequent_items, metric = "lift", min_threshold = 1)
rules.head()

rules.to_csv(r"C:\Users\acikgozs\Documents\mba_rules.txt")