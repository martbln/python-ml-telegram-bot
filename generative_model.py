from nltk import edit_distance

REPLICAS_LENGTH = 2
MAX_REPLICA_LENGTH = 25
MIN_REPLICA_LENGTH = 5
GENERATIVE_THRESHOLD = 0.7


def _is_good_length(replica):
    if MIN_REPLICA_LENGTH < len(replica) < MAX_REPLICA_LENGTH:
        return True
    return False


def check_replicas_length(replicas):
    if len(replicas) == REPLICAS_LENGTH:
        first_replica = replicas[0]
        second_replica = replicas[1]
        if _is_good_length(first_replica) and _is_good_length(second_replica):
            return True
    return False


def prepare_dialogues():
    with open('data/dialogues.txt') as f:
        dialogues_data = f.read()

    dialogues = []
    for dialogue in dialogues_data.split('\n\n'):
        replicas = []
        for replica in dialogue.split('\n')[:2]:
            replica = replica[2:].lower()
            replicas.append(replica)
        if check_replicas_length(replicas):
            dialogues.append(replicas)
    return dialogues


GENERATIVE_DIALOGUES = prepare_dialogues()


def get_answer_by_generative_model(text):
    text = text.lower()

    for question, answer in GENERATIVE_DIALOGUES:
        abs_value = abs(len(text) - len(question))
        if abs_value / len(question) < 1 - GENERATIVE_THRESHOLD:
            dist = edit_distance(text, question)
            question_length = len(question)
            similarity = 1 - dist / question_length
            if similarity > GENERATIVE_THRESHOLD:
                return answer
