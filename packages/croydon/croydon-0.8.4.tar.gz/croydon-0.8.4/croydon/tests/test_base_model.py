import asyncio
from typing import Optional
from unittest import IsolatedAsyncioTestCase
from pydantic import BaseModel as PydanticModel
from ..models.base_model import BaseModel
from ..models.fields import StringField
from ..models.index import Index, IndexDirection, IndexKey
from ..decorators import api_field


class TestBaseModel(IsolatedAsyncioTestCase):

    def test_empty(self):
        model = BaseModel()
        self.assertIsNone(model.id)
        self.assertCountEqual(model._fields, ["id"])

    def test_not_empty(self):
        class Model(BaseModel):
            field = StringField()

        model = Model({"field": "value"})
        self.assertEqual(model.field, "value")
        self.assertCountEqual(model._fields, ["id", "field"])

    def test_collection_name(self):
        class Model(BaseModel):
            COLLECTION = "models"

        bm = BaseModel()
        self.assertEqual(bm.collection, "base_model")

        m = Model()
        self.assertEqual(m.collection, "models")

    def test_rejected_fields(self):
        class Model(BaseModel):
            string_f = StringField()
            string_rf = StringField(rejected=True)

        model = Model()
        self.assertCountEqual(model._fields, ["id", "string_f", "string_rf"])
        self.assertTrue(model._fields["string_rf"].rejected)

    def test_restricted_fields(self):
        class Model(BaseModel):
            string_f = StringField()
            string_rf = StringField(restricted=True)

        model = Model()
        self.assertCountEqual(model._fields, ["id", "string_f", "string_rf"])
        self.assertTrue(model._fields["string_rf"].restricted)

    def test_indexes(self):
        class Model(BaseModel):
            string_f = StringField()
            string_if = StringField(index=True)
            string_uf = StringField(unique=True)
            string_duf = StringField(index=IndexDirection.DESCENDING, unique=True)

        model = Model()

        self.assertCountEqual(
            model._indexes,
            [
                Index(keys=[IndexKey(key="string_if", spec=IndexDirection.ASCENDING)]),
                Index(
                    keys=[IndexKey(key="string_uf", spec=IndexDirection.ASCENDING)],
                    options={"unique": True}
                ),
                Index(
                    keys=[IndexKey(key="string_duf", spec=IndexDirection.DESCENDING)],
                    options={"unique": True}
                ),
            ],
        )

    def test_to_dict(self):
        class Model(BaseModel):
            field1 = StringField()
            field2 = StringField()
            field3 = StringField(restricted=True)

        model = Model({"field1": "value1", "field2": "value2", "field3": "value3"})

        self.assertDictEqual(
            model.to_dict(), {"id": None, "field1": "value1", "field2": "value2"}
        )

        self.assertDictEqual(
            model.to_dict(fields=["field1", "field2", "field3"]),
            {"field1": "value1", "field2": "value2"},
        )

        self.assertDictEqual(
            model.to_dict(include_restricted=True),
            {"id": None, "field1": "value1", "field2": "value2", "field3": "value3"},
        )

        self.assertDictEqual(
            model.to_dict(fields=["field1", "field3"], include_restricted=True),
            {"field1": "value1", "field3": "value3"},
        )

        self.assertDictEqual(
            model.to_dict(
                fields=["field1", "field3", "bizzare"], include_restricted=True
            ),
            {"field1": "value1", "field3": "value3"},
        )

    async def test_api_field_methods(self):
        class Model(BaseModel):
            a = StringField()

            async def b(self):
                await asyncio.sleep(0.1)
                return "b"

            @api_field
            async def c(self):
                await asyncio.sleep(0.1)
                return "c"

        m = Model.create(a="a")
        self.assertDictEqual(m.to_dict(), {"id": None, "a": "a"})
        self.assertDictEqual(await m.to_dict_ext(), {"id": None, "a": "a"})
        self.assertDictEqual(
            await m.to_dict_ext(fields=["id", "a", "b", "c"]),
            {"id": None, "a": "a", "c": "c"},
        )

    async def test_from_pydantic(self):
        class Model(BaseModel):
            a = StringField(default="default_a")
            b = StringField(default="default_b")

        class PydanticPayload(PydanticModel):
            a: Optional[str]
            b: Optional[str]

        p = PydanticPayload(a="a")
        m = Model.from_pydantic(p)

        self.assertEqual(m.a, "a")
        self.assertEqual(m.b, "default_b")  # unset value in input must not override defaults
