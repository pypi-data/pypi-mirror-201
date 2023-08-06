import nicegui

# sample data
categories = {
    "Fruit": ["Apple", "Banana", "Orange"],
    "Vegetables": ["Carrot", "Broccoli", "Cucumber"],
    "Dairy": ["Milk", "Cheese", "Yogurt"],
}

# create a menu bar with entries for each category
menu = nicegui.MenuBar()
for category in categories:
    menu.add_entry(category)


# create a callback function to display the items in each category
@nicegui.react(menu)
def display_category(category):
    nicegui.set_output(f"{category}: {categories[category]}")


# set up the app layout with the menu bar and output area
nicegui.layout(menu, nicegui.Output())

# run the app
nicegui.app(title="Categorized Information")
