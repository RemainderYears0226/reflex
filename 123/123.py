import reflex as rx

class State(rx.State):

    items = []

    new_item: str

    updated_item: str

    def add_item(self, form_data: dict[str, str]):
        self.items.append(form_data["new_item"])

        return rx.set_value("new_item", "")

    def update_item(self, form_data: dict[str, str]):
        old_value = form_data["updated_item"].split(" -> ")[0]
        new_value = form_data["updated_item"].split(" -> ")[1]
        self.items[self.items.index(old_value)] = new_value

        return rx.set_value("updated_item", "")

    def finish_item(self, item: str):

        self.items.pop(self.items.index(item))


def todo_item(item: rx.Var[str]) -> rx.Component:
    return rx.list_item(
        rx.hstack(
            rx.button(
                "Delete",
                on_click=lambda: State.finish_item(item),
                height="1.5em",
                background_color="white",
                border="1px solid blue",
            ),
            rx.text(item, font_size="1.25em"),
        )
    )


def todo_list() -> rx.Component:
    return rx.ordered_list(
        rx.foreach(State.items, lambda item: todo_item(item)),
    )


def new_item() -> rx.Component:
    return rx.form(
        rx.input(
            id="new_item",
            placeholder="Add a todo...",
            bg="white",
        ),
        rx.center(
            rx.button("Add", type_="submit", bg="white"),
        ),
        on_submit=State.add_item,
    )

def updated_item() -> rx.Component:
    return rx.form(
        rx.input(
            id="updated_item",
            placeholder="Update a todo (old value -> new value)...",
            bg="white",
        ),
        rx.center(
            rx.button("Update", type_="submit", bg="white"),
        ),
        on_submit=State.update_item,
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Todos"),
            new_item(),
            updated_item(),
            rx.divider(),
            todo_list(),
            bg="#ededed",
            margin="5em",
            padding="1em",
            border_radius="0.5em",
            shadow="lg",
        )
    )


app = rx.App(state=State)

app.add_page(index, title="Todo App")

app.compile()
