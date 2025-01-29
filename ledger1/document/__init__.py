""" document module

Documents are handled by:

Document: contains the attributes, validations and basically:
 - set_from_reguest()
 - set_from_transaction
 - get_to_response()
 - get_to_transaction

    Primary attributes (stored in Transaction):
        doc_type: See TransactionType
        doc_num: cpart_nume + '.' + unique id number for the cpart
        dt
        ...


    Secondary attributes (stored in DocumentsField as name/value pairs):
        tdb

The seqs can be

    tra_seq: Debits/Credits in a Transaction
    tra_cod: Values in a transaction Document int eh format: base (+)adds - (-)subs = tot
    tra_acc: rows in an accunnt Document, like a bank sastement (tdb)


## TransactionType can currently be:
    inv1: Invoice
    dft: Electroinc Fund Transfer
    bstat: Bank statement (acsount document)


"""


