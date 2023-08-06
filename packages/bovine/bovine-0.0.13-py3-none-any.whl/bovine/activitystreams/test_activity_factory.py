from .activity_factory import ActivityFactory
from .object_factory import Object


def test_activity_factory_like():
    activity_factory = ActivityFactory({"id": "actor_id", "followers": "followers"})

    like = activity_factory.like("target")
    like.to.add("target")
    like.cc.add("other")
    like.content = "🐮"

    result = like.build()

    assert result["@context"] == "https://www.w3.org/ns/activitystreams"

    assert result["to"] == ["target"]
    assert result["cc"] == ["other"]

    assert result["type"] == "Like"


def test_activity_factory_accept():
    activity_factory = ActivityFactory({"id": "actor_id", "followers": "followers"})

    accept = activity_factory.accept({"id": "obj"})
    result = accept.build()

    assert result["@context"] == "https://www.w3.org/ns/activitystreams"
    assert result["type"] == "Accept"
    assert result["actor"] == "actor_id"
    assert result["object"]["id"] == "obj"


def test_activity_factory_create():
    activity_factory = ActivityFactory({"id": "actor_id", "followers": "followers"})
    note = (
        Object(type="Note", attributed_to="actor_id", followers="account/followers")
        .as_public()
        .build()
    )

    result = activity_factory.create(note).build()

    assert result["cc"] == ["account/followers"]
    assert result["to"] == ["https://www.w3.org/ns/activitystreams#Public"]
    assert result["actor"] == "actor_id"


def test_activity_factory_create_no_cc():
    activity_factory = ActivityFactory({"id": "actor_id", "followers": "followers"})
    remote_actor = "https://abel/alice"
    note = Object(
        type="Note",
        attributed_to="actor_id",
        followers="account/followers",
        to={remote_actor},
    ).build()

    result = activity_factory.create(note).build()

    assert result["cc"] == []
    assert result["to"] == [remote_actor]
    assert result["actor"] == "actor_id"
