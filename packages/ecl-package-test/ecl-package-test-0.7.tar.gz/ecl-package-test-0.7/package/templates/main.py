import evaluate
from template import ECLTrainer, TextClassificationDataset
from template.utils import (
    DataTrainingArguments,
    ModelArguments,
    compute_metrics,
    get_training_args,
)
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    HfArgumentParser,
)

if __name__ == "__main__":

    # arguments
    parser = HfArgumentParser((ModelArguments, DataTrainingArguments))
    model_args, data_args = parser.parse_args_into_dataclasses()
    training_args = get_training_args()

    ##LOGGER BLOCK
    logger = None
    ##END

    # tokenizer
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    # dataset
    train_dataset, test_dataset = TextClassificationDataset(
        data_args, mode="train"
    ), TextClassificationDataset(data_args, mode="test")
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    accuracy = evaluate.load("accuracy")

    # model
    id2label = {0: "NEGATIVE", 1: "POSITIVE"}
    label2id = {"NEGATIVE": 0, "POSITIVE": 1}

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased", num_labels=2, id2label=id2label, label2id=label2id
    )

    # Trainer
    trainer = ECLTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    # train
    trainer.train()
    model.save_pretrained("src/best_model")
