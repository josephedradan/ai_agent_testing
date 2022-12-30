"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/28/2022

Purpose:

Details:
start "H:\Programming\Python\projects_github\ai_testing\" cmd.exe /k py -3.8 "./multiagent/pacman.py"


start "H:\Programming\Python\projects_github\ai_testing\multiagent\" cmd.exe /k py -3.8 ".pacman.py"


H:\Programming\Python\projects_github\ai_testing\multiagent\pacman.py
Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
import os
import subprocess

LIST_PATH_RELATIVE_ASSIGNMENT = [
    "multiagent/"
]

# COMMAND_RUN = "start \"{}\" cmd.exe /k py -3.8 pacman.py"  # ONLY WORKS ON WINDOWS

LiST_ARG = [
    # "-p AgentPacmanGreedy",
    # "-p AgentPacmanLeftTurn",
    "-p AgentPacmanReflex",
    # "-p AgentPacmanReflex_Attempt_1",

]
# NOTES: /k will keep the shell when done.  /c will kill the shell when done
# COMMAND_RUN = "start cmd.exe /k py -3.8 pacman.py {} "  # ONLY WORKS ON WINDOWS
COMMAND_RUN = "start cmd.exe /c py -3.8 pacman.py {} "  # ONLY WORKS ON WINDOWS

def main():
    cwd = os.getcwd()

    ##########

    # Loop and run all the assignments as the same time
    for path_relative in LIST_PATH_RELATIVE_ASSIGNMENT:

        path_full_assignment = os.path.join(cwd, path_relative)
        # print("path_full_assignment", path_full_assignment)

        for arg in LiST_ARG:

            command = COMMAND_RUN.format(arg)

            print(command)

            # Execute command in corresponding directory
            subprocess.Popen(command,
                             cwd=path_full_assignment,
                             shell=True  # This must be true for the commands to work
                             )


if __name__ == '__main__':
    main()
