from control_box import ControlBox


class EditBox:
    def __init__(self, parent, id, text, styles, x, y, width, height):
        self.parent = parent
        self.id = id
        self.text = text
        self.styles = styles
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.control_type = "EDIT"
        self.control_box = ControlBox(self.parent, self.control_type, self.id)

    def create_edit_box(self):
        self.control_box.set_x(self.x)
        self.control_box.set_y(self.y)
        self.control_box.set_width(self.width)
        self.control_box.set_height(self.height)
        self.control_box.set_styles(self.styles)
        self.control_box.set_text(self.text)
        return self.control_box.create_control_box()
