import logging
import sys
import os

def rital():
    try:
        from datamaestro import prepare_dataset
    except:
        logging.info("Datamaestro n'est pas installé (cela ne devrait pas arriver)")
        sys.exit(1)

    for dataset_id in [
        "com.github.aagohary.canard",
        "irds.antique.train",
        "irds.antique.test",
    ]:
        logging.info("Preparing %s", dataset_id)
        prepare_dataset(dataset_id)

    try:
        from transformers import AutoTokenizer, AutoModelForMaskedLM
    except:
        logging.info("Datamaestro n'est pas installé (cela ne devrait pas arriver)")
        sys.exit(1)

    tokenizer = AutoTokenizer.from_pretrained("Luyu/co-condenser-marco")
    model = AutoModelForMaskedLM.from_pretrained("Luyu/co-condenser-marco")

    
def amal():
    try:
        from datamaestro import prepare_dataset
    except:
        logging.info("Datamaestro n'est pas installé (cela ne devrait pas arriver)")
        sys.exit(1)

    try:
        import datasets
    except:
        logging.info("datasets n'est pas installé (cela ne devrait pas arriver)")
        sys.exit(1)

    # From datamaestro
    for dataset_id in [
        "com.lecun.mnist",
        "edu.uci.boston",
        "org.universaldependencies.french.gsd",
        "edu.stanford.aclimdb",
        "edu.stanford.glove.6b.50"
    ]:
        logging.info("Preparing %s", dataset_id)
        prepare_dataset(dataset_id)

    # Hugging Face (CelebA)
    datasets.load_dataset("nielsr/CelebA-faces", os.environ.get("HF_DATASETS_CACHEDIR", None))
