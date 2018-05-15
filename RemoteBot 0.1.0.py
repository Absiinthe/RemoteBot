# -*- coding: utf-8  -*-

import asyncio, datetime, discord, getpass, logging, os, shutil, signal, struct, subprocess, threading, time, urllib.request, urllib.error, urllib.parse

user_bot = "RemoteBot" #Mettez dans cette variable le pseudo du bot.
token = "NDIzMTc1MjczMTk0ODQ4MjY2.DYmgWw.JUxtUf-MtSbDIvLScuozDqhnhPY" #Mettez dans cette variable le token du bot
trust = ["Utilisateur 1", "Utilisatur 2"]
only_PM = True

client = discord.Client()
ver = "0.1.0"
lang = "fr"

print("RemoteBot " + ver + " " + lang)

@client.event
@asyncio.coroutine
def on_message(message):
    rep = text = msg = message.content
    rep2 = text2 = msg2 = rep.split()
    user = str(message.author)
    user_bot_client = client.user.name
    trusted = user in trust
    try:
        server_msg = str(message.channel.server)
        chan_msg = str(message.channel.name)
        pm = False
    except AttributeError:
        server_msg = user
        chan_msg = user
        pm = True
    try:
        command = rep2[0].lower()
        params = rep2[0:]
    except IndexError:
        command = ""
        params = ""

    print(user + " (" + server_msg + ") [" + chan_msg + "] : " + rep)

    if not only_PM or pm:
        if command == "!cd" and trusted:
            try:
                try:
                    os.chdir(params[1].replace("_", " "))
                except IndexError:
                    os.chdir(os.getcwd())
                yield from client.send_message(message.channel, os.getcwd())
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!cmd" and trusted:
            try:
                command = os.popen(" ".join(params[1:]))
                for text in command.readlines():
                    yield from client.send_message(message.channel, text.strip("\n"))
                    time.sleep(1)
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if (command == "!connect" or command == "!download") and trusted:
            try:
                file_content = urllib.request.urlopen(urllib.request.Request(" ".join(params[1:]))).read()
                f = open(" ".join(params[1:]).split("/")[-1], "w")
                f.write(file_content)
                f.close()
                yield from client.send_message(message.channel, "Fichier enregistré.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!dir" and trusted:
            try:
                try:
                    listdir = " - ".join(os.listdir(params[1].replace("_", " ")))
                except IndexError:
                    listdir = " - ".join(os.listdir(os.getcwd()))
                yield from client.send_message(message.channel, listdir)
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!eval" and trusted:
            try:
                yield from client.send_message(message.channel, eval(" ".join(params[1:])))
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!exec" and trusted:
            try:
                exec(" ".join(params[1:]))
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if (command == "!exit" or command == "!quit") and trusted:
            exit()

        if command == "!fcontent" and trusted:
            try:
                if "/" not in params[1] and "\/" not in params[1]:
                    f = open(params[1].replace("_", " "), "r")
                    try:
                        start_line = int(params[2])
                    except IndexError:
                        start_line = 0
                    try:
                        stop_line = int(params[3])
                    except IndexError:
                        stop_line = None
                    i = 0
                    for line in f.readlines()[start_line:stop_line]:
                        yield from client.send_message(message.channel, line.strip("\n"))
                        time.sleep(1)
                        i += 1
                        if i >= 5:
                            yield from client.send_message(message.channel, "Fichier trop grand, utilisez !file " + params[1] + " pour envoyer tout le fichier.")
                            break
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!fcopy" and trusted:
            try:
                shutil.copyfile(params[1].replace("_", " "), params[2].replace("_", " "))
                yield from client.send_message(message.channel, "Fichier " + params[1].replace("_", " ") + " copié vers " + params[2].replace("_", " ") + ".")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!fcreate" and trusted:
            try:
                if "/" not in params[1] and "\/" not in params[1]:
                    f = open(params[1].replace("_", " "), "a")
                    f.close()
                    yield from client.send_message(message.channel, "Fichier " + params[1].replace("_", " ") + " crée.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!fdel" and trusted:
            try:
                if "/" not in params[1] and "\/" not in params[1]:
                    os.remove(params[1].replace("_", " "))
                    yield from client.send_message(message.channel, "Fichier " + params[1].replace("_", " ") + " supprimé.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!file":
            yield from client.send_file(message.channel, " ".join(params[1:]))

        if command == "!fren" and trusted:
            try:
                if "/" not in params[1] and "\/" not in params[1]:
                    os.rename(params[1].replace("_", " "), params[2].replace("_", " "))
                    yield from client.send_message(message.channel, "Fichier " + params[1].replace("_", " ") + " renommé en " + params[2].replace("_", " ") + ".")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!freplace" and trusted:
            try:
                if "/" not in params[1] and "\/" not in params[1]:
                    f = open(params[1].replace("_", " "), "r")
                    content = ""
                    for line in f.readlines():
                        content += line
                    f.close()
                    content = content.replace(params[2], params[3])
                    f = open(params[1], "w")
                    f.write(content)
                    f.close()
                    yield from client.send_message(message.channel, "Fichier " + params[1].replace("_", " ") + " modifié.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!fsize" and trusted:
            try:
                if "/" not in params[1] and "\/" not in params[1]:
                    yield from client.send_message(message.channel, str(os.path.getsize(params[1].replace("_", " "))) + " octet(s) dans " + params[1].replace("_", " "))
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!fwrite" and trusted:
            try:
                if "/" not in params[1] and "\/" not in params[1]:
                    f = open(params[1].replace("_", " "), "a")
                    f.write(params[2] + "\n")
                    f.close()
                    yield from client.send_message(message.channel, "Fichier " + params[1].replace("_", " ") + " modifié.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!irc" and trusted:
            try:
                threading.Thread(target=exec,args=("import HomeBot",)).start()
            except ImportError:
                yield from client.send_message(message.channel, "Vous devez télécharger HomeBot pour contrôler votre PC via IRC et Discord.")

        if command == "!kill" and trusted:
            try:
                os.kill(int(params[1]), signal.SIGTERM)
                yield from client.send_message(message.channel, "Processus " + params[1] + " arrêté.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!os_name":
            os_name = os.name
            if os_name == "nt":
                yield from client.send_message(message.channel, "OS : Windows")
            elif os_name == "posix":
                yield from client.send_message(message.channel, "OS : Linux")
            else:
                yield from client.send_message(message.channel, "OS : " + os_name)

        if command == "!rcreate" and trusted:
            try:
                os.mkdir(params[1].replace("_", " "))
                yield from client.send_message(message.channel, "Dossier " + params[1].replace("_", " ") + " crée.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!rdel" and trusted:
            try:
                shutil.rmtree(params[1].replace("_", " "))
                yield from client.send_message(message.channel, "Dossier " + params[1].replace("_", " ") + " supprimé.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!rren" and trusted:
            try:
                os.rename(params[1].replace("_", " "), params[2].replace("_", " "))
                yield from client.send_message(message.channel, "Dossier " + params[1].replace("_", " ") + " renommé en " + params[2].replace("_", " ") + ".")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!start" and trusted:
            try:
                subprocess.Popen(" ".join(params[1:]))
                yield from client.send_message(message.channel, "Programme " + " ".join(params[1:]) + " ouvert.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!todo_add" and trusted:
            try:
                f = open(todos_file_name, "a")
                f.write(" ".join(params[1:]))
                yield from client.send_message(message.channel, "Todo ajouté.")
                f.close()
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!todo_del" and trusted:
            try:
                f = open(todos_file_name, "r")
                task_file = f.read().split("\n")
                f.close()
                del(task_file[int(params[1])])
                f = open(todos_file_name, "w")
                f.write("\n".join(task_file))
                f.close()
                yield from client.send_message(message.channel, "Todo " + params[1] + " supprimé.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!todo_list" or command == "!todos":
            try:
                f = open(todos_file_name, "r")
                try:
                    start_line = int(params[2])
                except IndexError:
                    start_line = 0
                try:
                    stop_line = int(params[3])
                except IndexError:
                    stop_line = None
                i = 0
                for line in f.readlines()[start_line:stop_line]:
                    yield from client.send_message(message.channel, str(i) + " - " + line.strip("\n"))
                    time.sleep(1)
                    i += 1
                    if i >= 5:
                        yield from client.send_message(message.channel, "Fichier trop grand.")
            except:
                yield from client.send_message(message.channel, "Erreur.")

        if command == "!ver":
            yield from client.send_message(message.channel, "RemoteBot " + ver + " " + lang + ".")

client.run(token)
