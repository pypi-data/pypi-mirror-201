from queue import Empty
import jupyter_client

def execute(source):
    message_id = kernel_client.execute(source)
    try:
        reply = kernel_client.get_shell_msg(timeout=1.)
    except Empty:
        raise RuntimeError("Cell timed out: \n {}".format(source))


    if reply['content']['status'] != 'ok':
        traceback = reply['content']['traceback']
        description = "failed: '{}'\n\n Traceback:\n{}".format(source, '\n'.join(traceback))
        print(description)

    if reply['parent_header']['msg_id'] != message_id:
        description = "failed: REPLY FROM A WRONG ID'{}'\n\n Traceback:\n{}".format(source, '\n'.join(traceback))
        print(description)

    #if reply['header']['msg_type']
    #else: print("Message type is not execute result. ", reply['header']['msg_type'])

    while True:
        try:
            io_msg = kernel_client.get_iopub_msg(timeout=1)
            match io_msg['msg_type']:
                case 'status':
                    match io_msg['content']['execution_state']:
                        case 'busy': pass
                        case 'idle': break
                        case _: continue
                case "execute_result":
                    print("RESULT:", io_msg['content']['data'].get('text/plain', ''))
                case "stream":
                    print("RESULT:", io_msg['content']['text'])
                case _: print(io_msg['msg_type'], io_msg['content'])
        except Empty:
            print('timeout kc.get_iopub_msg')
            break


if __name__ == '__main__':
    kernel_manager, kernel_client = jupyter_client.manager.start_new_kernel(kernel_name='python3', startup_timeout=15)

    # When I initially tried this, I got a permission error. This was fixed by installing the python3 kernel spec (apparently Jupyter does not do this automatically...):
    # python3 -m ipykernel install --user
    # And then you can get the ports by

    print(kernel_manager.get_connection_info())

    print("Kernel is alive: {0}".format(kernel_manager.is_alive()))


    text = """
    %load_ext magics
    @```python
    print('Hello World!')
    ```
    %unload_ext magics
    """

    execute(text)

    print('stop channels')
    kernel_client.stop_channels()

    kernel_manager.shutdown_kernel(now = True)

    # So there are several parts to it.  
    # 1. We need to start the kerel and pipe GPT to it.
    # 2. This kernel should have our custom prompt & magics + support normal stuff.  GPT prompt is our kernel prompt
    # 3. This kernal should have pyros in the event loop and space  (based on https://github.com/RoboStack/jupyter-ros ?)
    # 4. When kernel dies, it should bring down ROS node
    # 5. We restart and inform GPT
