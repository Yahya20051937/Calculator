from types import coroutine


@coroutine
def display(root, label):
    from main import get_func2
    e_string = ''
    e_list = []

    func = get_func2(root, label)
    while True:
        e = yield
        if e != 'res' and e != 'c':
            e_string += str(e)
            e_list.append(e)
            label.config(text=f'{e_string}')
            root.update()
        else:
            if e == 'res':
                func.send(e_list)
                e_string = ''
                e_list = []

            else:
                e_list = []
                e_string = ''
                label.config(text='')
                root.update()


async def display_async(g):
    await g
