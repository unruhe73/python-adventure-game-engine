# **Name vs ID**

When you act on an item in a room you act in its name.
Example:
  describe crystal

Items in a rooms are stored into PlayGame class as a list of IDs. Two IDs have to be different. Names can be the same.
Suppose you have a blue crystal and white crystal. When you refer to crystal you don't know which one you want.
If you have more crystals and each is in a different room you don't have any problem if you want a description.

What happen when you catch it and it goes into the inventory list?
In this case when you ask for a description than the description act looks for the corresponding ID of that
name first into the inventory. So if you have a crystal in the inventory and a crystal into the room you will get
the description of your inventory crystal. Of course it's wrong. If you want to know more details of the
white crystal in the room you get more details of the blue crystal into the inventory.

This is a known but. At the moment this Python Adventure Game Engine is in a developing step, so things can change
anytime of course bugs will be fixed during my spare time when I have it.

I want to create a valid Python Adventure Game Engine. If you want you can suggest or give help.

**Update: 4h Nov 2022**

Part of the "*name vs id*" bug has been fixed. Now you can say:
describe white crystal

and the engine goes into the inventory looking for the white crystal. Next step is to fix this in case
you have in the scene two crystal with different colours.