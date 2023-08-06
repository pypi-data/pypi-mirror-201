from unittest.mock import patch
from ..models.storable_model import StorableModel
from ..models.fields import StringField, Field, ObjectIdField
from ..db import ObjectsCursor
from ..decorators import allow_as_field
from .mongo_mock_test import MongoMockTest


CALLABLE_DEFAULT_VALUE = 4


def callable_default():
    return CALLABLE_DEFAULT_VALUE


class TestModel(StorableModel):
    field1 = StringField(rejected=True, index=True, default="default_value")
    field2 = Field(required=True)
    field3 = Field(required=True, default="required_default_value")
    callable_default_field = Field(default=callable_default)


class TestStorableModel(MongoMockTest):

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        await TestModel.destroy_all()

    async def asyncTearDown(self) -> None:
        await TestModel.destroy_all()
        await super().asyncTearDown()

    async def test_defaults(self):
        model = TestModel()
        self.assertEqual("default_value", model.field1)
        self.assertEqual("required_default_value", model.field3)
        self.assertEqual(CALLABLE_DEFAULT_VALUE, model.callable_default_field)

    async def test_eq(self):
        model = TestModel({"field2": "mymodel"})
        await model.save()
        model2 = await TestModel.find_one({"field2": "mymodel"})
        self.assertEqual(model, model2)

    async def test_reject_on_update(self):
        model = TestModel.create(field1="original_value", field2="mymodel_reject_test")
        await model.save()
        id_ = model.id
        await model.update({"field1": "new_value"})
        model = await TestModel.find_one({"_id": id_})
        self.assertEqual(model.field1, "original_value")

    async def test_update_many(self):
        model1 = TestModel.create(field1="original_value", field2="mymodel_update_test")
        await model1.save()
        model2 = TestModel.create(field1="original_value", field2="mymodel_update_test")
        await model2.save()
        model3 = TestModel.create(field1="do_not_modify", field2="mymodel_update_test")
        await model3.save()

        await TestModel.update_many(
            {"field1": "original_value"}, {"$set": {"field2": "mymodel_updated"}}
        )
        await model1.reload()
        await model2.reload()
        await model3.reload()

        self.assertEqual(model1.field2, "mymodel_updated")
        self.assertEqual(model2.field2, "mymodel_updated")
        self.assertEqual(model3.field2, "mymodel_update_test")

    @patch("croydon.context.ctx._cache_l2", spec=True)
    @patch("croydon.context.ctx._cache_l1", spec=True)
    async def test_invalidate(self, l1c, l2c):
        class Model(StorableModel):
            field1 = StringField()
            KEY_FIELD = "field1"

        model = Model({"field1": "value"})
        await model.save()

        l1c.delete.assert_called_once_with("model.value")
        l2c.delete.assert_called_once_with("model.value")

        await model.save()
        l1c.delete.assert_any_call(f"model.{model.id}")
        l1c.delete.assert_any_call("model.value")
        l2c.delete.assert_any_call(f"model.{model.id}")
        l2c.delete.assert_any_call("model.value")

    async def test_update(self):
        model = TestModel.create(field1="original_value", field2="mymodel_update_test")
        await model.save()
        id_ = model.id
        await model.update({"field2": "mymodel_updated"})
        model = await TestModel.find_one({"_id": id_})
        self.assertEqual(model.field2, "mymodel_updated")

    async def test_count(self):
        class Model(StorableModel):
            a = Field()

        for i in range(100):
            m = Model.create(a=i)
            await m.save()

        cur = Model.find({})
        count = await cur.count()
        self.assertEqual(count, 100)

        cur = Model.find({"a": {"$lt": 10}})
        count = await cur.count()
        self.assertEqual(count, 10)

    async def test_to_dict_ext_cursor_properties(self):
        class DepModel(StorableModel):
            a = Field()
            master_id = ObjectIdField(required=True)

        class MasterModel(StorableModel):
            name = Field()

            @allow_as_field
            def deps(self) -> ObjectsCursor["DepModel"]:
                return DepModel.find({"master_id": self.id})

        master = MasterModel.create(name="master")
        await master.save()

        for i in range(10):
            dep = DepModel.create(a=i, master_id=master.id)
            await dep.save()

        # check normal method usage
        deps = await master.deps().all()
        self.assertEqual(len(deps), 10)

        # check deps are accessible via API
        dct = await master.to_dict_ext(fields=["id", "name", "deps"])
        self.assertEqual(len(dct["deps"]), 10)
