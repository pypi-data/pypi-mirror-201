# MusiSort : Using K-Means Clustering to automatically categorize digital music files.

# Abstract

Downloading music is done by many different people for many different reasons, whether it be for backups, data hoarding, or to listen to music while offline. However, those who do download music, come across the issue of organizing all the files into categories that they can reference when needed. The most known way to organize music is by genres. The issue with genres however, is that they are set by humans and liable to be incorrect, or there could be no genre assigned to the audio file based on how it was retrieved. Currently, if you want to find what genre a song belongs to, you have to manually search for it online and assign it to the song through a tool. While this may work for a short list of songs, if you have a larger list (say about 1000 songs), this process becomes much more time consuming. MusiSort aims to fix this issue by automatically sorting songs into categories based not on genre, but by musical similarity. It accomplishes this task by utilizing new and known musical analysis methods to generate data and feed that information to K-Means Clustering to generate categories. Through this, MusiSort can take a large list of audio files, and separate them by melodies, tempo, mood, and more.

# Description and Thesis

MusiSort is a tool being developed to collect music and put them into similar groups or clusters based on their waveform.  The program uses artifical intelligence to check similarities and differences between the different songs.  The main goal of the project is to create a tool which removes the need to manually sort music into different genres as this can be quite a difficult, and tedious, task.  

Thesis : https://github.com/ReadyResearchers/cmpsc-600-fall-2022-and-spring-2023-senior-thesis-gvanzin-allegheny

# Installation

As MusiSort is a pip tool, it can be easily installed with the help of Python and Pip through the following command:

`pip install musisort`

MusiSort files are stored under the user directory as `musisort`.  For instance, on windows, `C:\\Users\\ComputerName\\AppData\\Local\\user\\musisort`.

# Usage

**MusiSort Command Line Interface**

There are a total of 7 different commands currently available to use in musisort. The following is a list of each command:

- musisort help
- musisort info <command>
- musisort dir
- musisort config <key> <value>
- musisort analyze
- musisort classify <list_name> <cluster_count>
- musisort debug

`help`  : displays the commands in musisort along with a description of what each one does.

`info`  : when used with a command as an argument, displays a more in-depth description of the command compared to the help menu.

`dir`   : lists all directories on the system associated with MusiSort.

`config`: when used without arguments, shows current config values in the terminal. If used with the key and value arguments, changes that key's value in the config.

`analyze`: retrieves song data from the folder `all\songs` and uses the classes under the analysis_methods folder in MusiSort's code to analyze each song.

`classify`: takes song's stored in the list/folder specified in the arguments and clusters them based on the amount given in the command.  To classify, each song in the list must first be analyzed with the analyze command.

`debug` : uses a song located in the debug folder of MusiSort's directory to run tests and check MusiSort's performance\accuracy.

**Using MusiSort to Classify Songs**

1. Open terminal and run the command `musisort dir`.  Go to the directory located under the `All Songs List Folder` called `Songs Folder`.  An example of this path on Linux would be : `/home/user/.local/share/musisort/songlists/all/songs`.
2. Add all songs you want to sort into this folder.
3. Run `musisort analyze`.  The first time this is run, it will go through every song and gather data about it.  Everytime you add a new song to `all/songs`, this command will need to be run again to analyze the newly added songs.
4. After the analyzation is completed, run `musisort classify <song_list> <catergory_count>`.  For this example, we will use `musisort classify all 5`.  Since our songs are located in the directory `songlists/all/songs`, the list name is `all` as that is the name of the folder the songs are located in.  The 5 means we will be categories ranging from 0 to 4 returned to use for each song.  If the value -1 is used for the `category_count` argument, the program will attempt to automatically assign a number of categories.  Once the program has finished classification, it will display the categories to the console in a list as so:

![Screenshot from 2023-04-0934754 15-12-33](https://user-images.githubusercontent.com/54772966/230233534-506b809e-8f1f-4231-9905-58c659328a55.png)

**Data Used for Testing**

https://drive.google.com/drive/folders/1kCke4O5IVPndeUuDvmzUe2n7M6pokksR?usp=share_link

The folder containing data is split into two sections.  The folder `Accuracy Song` contains the audio file used to test the program using the `musisort debug` command.  To use the debug command using this file, drag the song located in the folder into the `songlists\debug\songs` folder in the MusiSort directory.  Then you can run `musisort debug` to get data related to the accuracy of the classification and analysis methods.

Inside the `Efficiency Data` folder, 4 different zip files contain 1, 5, 10, and 25 songs.  The speed of the program was determined by placing various `sys.time` checks within the code of MusiSort and running the program with these set amount of audio files.  This can be done by cloning the MusiSort repository, and then running `pip install .` or `pip install --upgrade .` in the cloned directory when adding time checks in the locally stored code.

# Current Development State

[✅] Develop the algorithm to sort songs into categories.

[✅] Optimize the algorithms used to sort songs for faster completion.

[✅] Create a more user friendly terminal interface for easier usage.

[✅] Display list of labels in terminal after classification has finished.

[✅] Develop framework for testing accuracy of data analysis methods and classification. - Current Release 1.0

[🏗️] Add option to append classification labels onto audio file's metadata genre tag.

[🏗️] Explore implementation of other clustering methods.

[❌] Develop a GUI for more interactivity with the program.

(🏗️ : in progress , ❌ : not started yet , ✅ : completed)

# Related Work

Spotify's 15 Personalized Mood Filters

https://newsroom.spotify.com/2021-02-25/how-to-sort-your-favorite-songs-with-spotifys-new-genre-and-mood-filters/

Sony’s 12 Tone Analysis

https://www.sony.com/electronics/support/articles/00009093

Jiang, Yanru & Jin, Xin. (2022). Using k-Means Clustering to Classify Protest Songs Based on Conceptual and Descriptive Audio Features. 10.1007/978-3-031-05434-1_19. 

https://www.researchgate.net/publication/361335249_Using_k-Means_Clustering_to_Classify_Protest_Songs_Based_on_Conceptual_and_Descriptive_Audio_Features

Kim, Kyuwon, et al. “Clustering Music by Genres Using Supervised and Unsupervised Algorithms.” Standford, pp. 1–5. 

https://cs229.stanford.edu/proj2015/129_report.pdf

# Dependencies Used

- Librosa  : https://librosa.org/doc/latest/index.html
- Sklearn  : https://scikit-learn.org/stable/
- Scipy    : https://scipy.org/
- Numpy    : https://numpy.org/
- Appdirs  : https://pypi.org/project/appdirs/
- Progress : https://pypi.org/project/progress/

