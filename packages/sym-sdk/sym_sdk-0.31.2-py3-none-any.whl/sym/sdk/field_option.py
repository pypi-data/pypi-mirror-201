from pydantic import BaseModel


class FieldOption(BaseModel):
    """A Pydantic model representing an option to display in a dynamic Slack drop-down menu.

    FieldOptions are returned by Prefetch Reducers to dynamically
    generate a list of options for Prompt Fields with `prefetch = true`.
    """

    value: str
    """The actual value to pass through when selected."""

    label: str
    """A short label to display in the Slack drop-down menu.

    The label will be used to filter the options to display when a requester types into the Slack input box.
    """
