from enum_.shared.utils import run_command

def sudo_enum(password):
    if not password:
        return {"Sudo List": "Password not provided, if you know it run Riff with -p [PASSWORD]"}

    sudo_l = run_command(["sudo", "-lS"], input_text=password + "\n")


    return {"Sudo List": sudo_l}