# Discord meeting-helper

It was designed to work with GitLab, it gets the active issues from it, plus you can add your own topics if you want. This has to be set through discord with a Personal Access Token.

### Instructions
Set the personal access token first with **!config** \<token\>

You can see these commands with **!commands**

You can add topics to the agenda with the command: **!addtopic** \<topic-text\>
  
You can see the current topics on the agenda with: **!showagenda**

You can clear the agenda with: **!clearagenda**

You can delete topics from the agenda with: **!deletetopic** (you will be prompted after sending this command)

You can see the full agenda (gitlab boards aswell) with: **!topic**

#### PS

This bot was custom made for our needs, so you will probably have to change some code within it to work correctly. Mainly in the file prioritylevels.py, you can see that we used the labels "In Verification" and "In Progress", which were the names of labels/boards in our GitLab project.
