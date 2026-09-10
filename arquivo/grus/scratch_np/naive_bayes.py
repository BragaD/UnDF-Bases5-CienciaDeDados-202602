"""Naive Bayes com numpy — o que o capítulo 10 ensina.

A seção 10.3 escreve `tokenize`, `Message`, `NaiveBayesClassifier` e `predict`
inline; as seções 10.4 e 10.5 importam daqui. O código é o mesmo dos chunks — o
módulo é o chunk salvo em arquivo. Nenhum outro capítulo importa deste módulo.

O modelo não sorteia nada: a divisão treino/teste é de quem chama, com o `rng`
de `scratch_np.machine_learning.split_data`.
"""
from typing import Iterable, NamedTuple, Set, Tuple
from collections import Counter
import re

import numpy as np


def tokenize(text: str) -> Set[str]:
    text = text.lower()                          # Converte para minúsculas,
    all_words = re.findall("[a-z0-9']+", text)   # extrai as "palavras", e
    return set(all_words)                        # remove as duplicadas.


assert tokenize("Data Science is science") == {"data", "science", "is"}


class Message(NamedTuple):
    text: str
    is_spam: bool


class NaiveBayesClassifier:
    def __init__(self, k: float = 0.5) -> None:
        self.k = k  # fator de suavização

        self.tokens: np.ndarray = np.array([], dtype=str)
        self.token_spam_counts: np.ndarray = np.array([], dtype=int)
        self.token_ham_counts: np.ndarray = np.array([], dtype=int)
        self.spam_messages = self.ham_messages = 0

    def train(self, messages: Iterable[Message]) -> None:
        spam_counts: Counter = Counter()
        ham_counts: Counter = Counter()

        for message in messages:
            # Incrementa as contagens de mensagens
            if message.is_spam:
                self.spam_messages += 1
            else:
                self.ham_messages += 1

            # Incrementa as contagens de palavras
            for token in tokenize(message.text):
                if message.is_spam:
                    spam_counts[token] += 1
                else:
                    ham_counts[token] += 1

        # A varredura acabou e o vocabulário está fechado: ele vira um array
        # ORDENADO, e as duas contagens viram arrays alinhados a ele — a
        # posição i é sempre o token self.tokens[i], em todos os três.
        self.tokens = np.array(sorted(spam_counts.keys() | ham_counts.keys()))
        self.token_spam_counts = np.array([spam_counts[t] for t in self.tokens],
                                          dtype=int)
        self.token_ham_counts = np.array([ham_counts[t] for t in self.tokens],
                                         dtype=int)

    def _probabilities(self) -> Tuple[np.ndarray, np.ndarray]:
        """P(token | spam) e P(token | ham) para todo o vocabulário, de uma vez."""
        p_token_spam = (self.token_spam_counts + self.k) / (self.spam_messages + 2 * self.k)
        p_token_ham = (self.token_ham_counts + self.k) / (self.ham_messages + 2 * self.k)

        return p_token_spam, p_token_ham


def predict(self, text: str) -> float:
    p_spam, p_ham = self._probabilities()

    # A máscara: True nas posições cujo token aparece na mensagem.
    presentes = np.isin(self.tokens, list(tokenize(text)))

    # Presente: soma log(p). Ausente: soma log(1 - p). Numa redução só.
    log_prob_if_spam = np.sum(np.where(presentes, np.log(p_spam), np.log(1 - p_spam)))
    log_prob_if_ham = np.sum(np.where(presentes, np.log(p_ham), np.log(1 - p_ham)))

    prob_if_spam = np.exp(log_prob_if_spam)
    prob_if_ham = np.exp(log_prob_if_ham)
    return float(prob_if_spam / (prob_if_spam + prob_if_ham))


NaiveBayesClassifier.predict = predict


# O exemplo de brinquedo da seção 10.4 — o render é o teste.
_messages = [Message("spam rules", is_spam=True),
             Message("ham rules", is_spam=False),
             Message("hello ham", is_spam=False)]

_model = NaiveBayesClassifier(k=0.5)
_model.train(_messages)

assert np.array_equal(_model.tokens, np.array(["ham", "hello", "rules", "spam"]))
assert _model.spam_messages == 1
assert _model.ham_messages == 2
assert np.array_equal(_model.token_spam_counts, np.array([0, 0, 1, 1]))
assert np.array_equal(_model.token_ham_counts, np.array([2, 1, 1, 0]))

# As probabilidades de "hello spam", na ordem do vocabulário.
_probs_if_spam = np.array([
    1 - (0 + 0.5) / (1 + 2 * 0.5),  # "ham"   (ausente)
    (0 + 0.5) / (1 + 2 * 0.5),      # "hello" (presente)
    1 - (1 + 0.5) / (1 + 2 * 0.5),  # "rules" (ausente)
    (1 + 0.5) / (1 + 2 * 0.5),      # "spam"  (presente)
])
_probs_if_ham = np.array([
    1 - (2 + 0.5) / (2 + 2 * 0.5),  # "ham"   (ausente)
    (1 + 0.5) / (2 + 2 * 0.5),      # "hello" (presente)
    1 - (1 + 0.5) / (2 + 2 * 0.5),  # "rules" (ausente)
    (0 + 0.5) / (2 + 2 * 0.5),      # "spam"  (presente)
])

_p_if_spam = np.exp(np.sum(np.log(_probs_if_spam)))
_p_if_ham = np.exp(np.sum(np.log(_probs_if_ham)))

# Deve dar aproximadamente 0,835 — e comparado com tolerância, não com ==.
assert np.isclose(_model.predict("hello spam"),
                  _p_if_spam / (_p_if_spam + _p_if_ham))
