from ..utils import *

# from utils import *
import html

from .. import regex as re_

# import regex as re_

from ..data.ingredient_funnel import dictionary as ing_funnel

# from data.ingredient_funnel import dictionary as ing_funnel
from ..data.categories import models

# from data.categories import models
import numpy as np
import unicodedata
from unidecode import unidecode

from ..data.categories import (
    title_map,
    root_map,
    ing_keys,
    ing_map,
    exceptions,
    function_map,
)

from ..data.categories import proteins
import spacy
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
en_core_web_sm = os.path.join(ROOT_DIR, "models", "en_core_web_sm")
nlp = spacy.load(en_core_web_sm)


class RecipeReader:
    def __init__(self):
        self._attributes = ["quantity", "unit", "size", "color", "ingredient", "simple"]
        pass

    def normalize(self, phrase):
        phrase = unicodedata.normalize("NFD", phrase)
        phrase = unidecode(phrase)
        phrase = phrase.lower()
        phrase = re.sub(r"\([^)]*\)", "", phrase)
        phrase = re.sub(r"\(|\)", "", phrase)

        for vulgar_fraction, fraction_str in vf.dictionary.items():
            phrase = re.sub(vulgar_fraction, " " + fraction_str + " ", phrase)

        phrase = phrase.replace("–", "-")
        phrase = phrase.replace("⁄", "/")
        phrase = re.sub(r"half ?(?:and|-) ?half", "half-and-half", phrase)
        phrase = re.sub(r"\.\.+", "", phrase)
        phrase = re.sub(r" *\. *(?![0-9])", ". ", phrase)
        phrase = re.sub(r"(?<=[0-9]) *\. *(?=[0-9])", ".", phrase)
        phrase = re.sub(r" '", "'", phrase)
        phrase = re.sub(r"(,[^,]+)?< ?a href.*", "", phrase)
        phrase = re.sub(r""" *<(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+> *""", "", phrase)
        phrase = re.sub(r"(?<=[a-z])/[a-z]+", "", phrase)
        phrase = re.sub(r"\b(?:5|five)[- ]?spice", "fivespice", phrase)
        phrase = re.sub(r".*: ?", "", phrase)
        phrase = re.sub(r"\s+", " ", phrase)
        phrase = phrase.strip()
        return phrase

    def merge_ingredients(self, ingredients):
        out = []
        outIngs = []

        for ing in ingredients:
            if ing["simple"] not in outIngs:
                out += [ing.copy()]
                outIngs += [ing["simple"]]
            else:
                for i, o in enumerate(out):
                    if o["simple"] == ing["simple"] and o["unit"] == ing["unit"]:
                        if not ing["quantity"] or not o["quantity"]:
                            continue
                        out[i]["quantity"] += ing["quantity"]

        return out

    def read_phrase(self, phrase):
        if not P_filter(str(phrase)):
            return None

        phrase = html.unescape(phrase)
        phrase = self.normalize(phrase)
        phrase = P_duplicates(phrase)

        phrase = P_multi_misc_fix(phrase)
        phrase = P_multi_misc_fix(phrase)
        phrase = P_missing_multiplier_symbol_fix(phrase)
        phrase = P_quantity_dash_unit_fix(phrase)
        phrase = P_juice_zest_fix(phrase)

        values = re.search(re_.INGREDIENT, phrase).groupdict()

        values["unit"] = None
        if values["quantity"]:
            values["quantity"], values["unit"] = re.search(
                rf"(?P<quantity>{re_.Q})? ?(?P<unit>.*)?", values["quantity"]
            ).groups()
            values["quantity"] = Q_to_number(values["quantity"])

        values["unit"] = U_unify(values["unit"])
        values["quantity"], values["unit"] = Q_U_unify(
            values["quantity"], values["unit"]
        )

        values["size"] = S_unify(values["size"])

        if values["ingredient"] != values["ingredient"] or not values["ingredient"]:
            return None

        values["ingredient"] = I_to_singular(values["ingredient"])
        values["simple"] = I_label_protein(values["ingredient"])
        values["simple"] = I_simplify(values["simple"])

        if values["simple"] == "sugar":
            values["quantity"], values["unit"] = Q_U_sugar(
                values["quantity"], values["unit"]
            )

        values["simple"] = re.sub(r"\bnan\b", "naan", values["simple"])

        filtered = {c: values[c] for c in self._attributes}
        filtered["simple"] = values["simple"]
        return filtered

    def funnel(self, phrase):
        return ing_funnel[phrase] if phrase in ing_funnel else None

    def clean_title(self, title):
        title = squish_multi_bracket(title)
        title = rm_nested_bracket(title)
        title = rm_bracket_content(title)
        title = rm_roman_numerals(title)
        title = re.sub(r" \|.+$", "", title)
        title = re.sub(r"\bRecipe\b", "", title)
        title = re.sub(r"\s+", " ", title)
        title = html.unescape(title)
        title = rm_accent(title)
        title = title.strip(" ")
        title = title.lower()
        title = re.sub(r"\bnan\b", r"\bnaan\b", title)
        return title

    def alt_title(self, title):
        title = squish_multi_bracket(title)
        title = (
            re.search(r"(?:\((?P<alt_title>.*)\))?$", title)
            .groupdict()
            .get("alt_title", "")
        ) or ""
        return title.lower()

    def categorize(self, title, ingredients, steps, parsedPhrases):
        categories = []
        alt_title = self.alt_title(title)
        title = self.clean_title(title)
        roots = [token.text.lower() for token in nlp(title) if token.dep_ == "ROOT"] + [
            token.text.lower() for token in nlp(alt_title) if token.dep_ == "ROOT"
        ]

        if any(re.search(to_regex(exceptions), root) for root in roots):
            return ["niche"]

        for key in ing_keys:
            for ing in ingredients:
                if key == ing:
                    categories.append(key)
                    break

        for key, regex in ing_map.items():
            for ing in ingredients:
                if ing == regex:
                    categories.append(key)
                    break

        for key, regex in root_map.items():
            match = re.search(regex, title)
            if not match:
                continue
            if any(root in match[0] for root in roots):
                categories.append(key)
                break

            if re.search(rf"{regex}$", title) and not re.search(
                r"\band\b|\bwith\b|&", title
            ):
                categories.append(key)

        for key, regex in title_map.items():
            if re.search(regex, title) or re.search(regex, alt_title):
                categories.append(key)

        for key, labelF in function_map.items():
            if labelF(parsedPhrases):
                categories.append(key)

        if any(p in categories for p in proteins):
            categories = [c for c in categories if c != "vegetarian"]

        if not len(categories):
            categories = ["vegetarian"]

        return list(set(categories))

    def categories_to_models(self, categories_a):
        out = []
        for category in categories_a:
            for model, categories_b in models.items():
                if category in categories_b:
                    out.append(model)

        return out if len(out) > 0 else ["other"]

    def read(self, title, phrases, steps=[]):
        parsedPhrases = [self.read_phrase(p) for p in phrases]
        parsedPhrases = self.merge_ingredients([p for p in parsedPhrases if p])
        columns = sorted(list(set(list(ing_funnel.values()))))

        ingredients = [
            self.funnel(p["simple"]) for p in parsedPhrases if self.funnel(p["simple"])
        ]
        categories = self.categorize(title, ingredients, steps, parsedPhrases)

        if "niche" in categories:
            categories = ["niche"]

        return {
            "ingredients": ingredients,
            "ingredients_": parsedPhrases,
            "title": title,
            "categories": categories,
            "models": self.categories_to_models(categories),
            "values": np.array([1 if c in ingredients else 0 for c in columns]),
        }


from sentence_transformers import SentenceTransformer
import pandas as pd
from ..data.embeddings import mean_ing_embedding
from qdrant_client import QdrantClient


ING_EMBEDDING_LEN = 128
TAG_EMBEDDING_LEN = 384


class TagReader:
    def __init__(
        self,
        ing_model,
        qdrant_host="qdrant.pocketsomm.dev",
        qdrant_port=443,
        qdrant_https=True,
    ):
        tag_model_path = os.path.join(ROOT_DIR, "models", "tag_embedding.model")
        self.tag_model = SentenceTransformer(tag_model_path)
        self.ing_model = ing_model

        embedding_csv_path = os.path.join(
            ROOT_DIR, "data", "mean_ing_embedding_per_tag.csv"
        )
        self.__mean_ing_e_per_tag = pd.read_csv(embedding_csv_path, index_col=[0])
        self.tags = list(self.__mean_ing_e_per_tag.columns)
        self.__mean_ing_e = np.array(mean_ing_embedding)

        self.qdrant = QdrantClient(
            host=qdrant_host, port=qdrant_port, https=qdrant_https
        )

    def generate_ing_embedding(self, ing):
        return self.ing_model.wv[ing] if ing in self.ing_model.wv else None

    def generate_tag_embedding(self, tag):
        return self.tag_model.encode(tag)

    def get_ing_embedding_of_tag(self, tag):
        return self.__mean_ing_e_per_tag[tag].values

    def preprocess_tags(self, tags):
        processed_tags = []
        for tag in tags:
            closest_tag = self.get_closest_tag(tag)
            if closest_tag == tag:
                processed_tags.append(closest_tag)
            else:
                tag = " ".join(
                    [tag.text.strip() for tag in nlp(tag) if not tag.is_stop]
                )
                closest_tags = self.get_closest_tags(tag, n=len(tag.split()))
                processed_tags += closest_tags

        return processed_tags if processed_tags else tags

    def get_ing_embedding_by_tags(self, tags):
        embeddings = []
        for tag in self.preprocess_tags(tags):
            embedding = self.get_ing_embedding_of_tag(tag) - self.__mean_ing_e
            embeddings.append(embedding)

        embedding_sum = sum(embeddings)
        return np.add(embedding_sum, self.__mean_ing_e)

    def get_closest_tags(self, tag, n):
        results = self.qdrant.search(
            collection_name=f"tag",
            query_vector=self.tag_model.encode(tag),
            limit=n,
            with_payload=True,
        )

        return [r.payload["value"] for r in results]

    def get_closest_tag(self, tag):
        return self.qdrant.search(
            collection_name=f"tag",
            query_vector=self.tag_model.encode(tag),
            limit=1,
            with_payload=True,
        )[0].payload["value"]

    def read(self, tags):
        embedding = self.get_ing_embedding_by_tags(tags)
        search_results = self.qdrant.search(
            collection_name="recipe-ing",
            query_vector=("embedding", embedding.tolist()),
            limit=5,
            with_vectors=True,
            with_payload=True,
        )

        model_list = flatten([r.payload["models"] for r in search_results])
        most_frequent = max(set(model_list), key=model_list.count)

        for r in search_results:
            if most_frequent in r.payload["models"]:
                values = r.vector["oneHot"]
                mask = values != 0
                values[mask] = 1.0
                return {"values": np.array(values), "models": [most_frequent]}
