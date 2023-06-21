def pack_elements1(sub_frame, *args):
    sub_frame.pack(side='top', fill='both', expand=True)
    for item in args:
        item.pack(side='left', fill='both', expand=True)



