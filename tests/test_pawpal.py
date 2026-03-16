from pawpal_system import Task, Pet


def test_mark_complete():
    task = Task("Feed", "feeding", "08:00")

    task.mark_complete()

    assert task.completed is True


def test_add_task_to_pet():
    pet = Pet("Buddy", "Dog", 4)

    task = Task("Walk", "walk", "07:00")

    pet.add_task(task)

    assert len(pet.tasks) == 1