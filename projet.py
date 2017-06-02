#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from io import StringIO
import time


def extAsciiCompress(chaine):
    """
    Cette fonction va compresser une chaine de caractère placée en
    entrée. La sortie de cette fonction est une C{list} en ASCII étendue.
    Pour vérifier le bon fonctionnement de cet algorithme, il est possible
    d'ajouter les lignes suivantes à la fonction I{main} de ce script :
    I{chaine = "TOBEORNOTTOBEORTOBEORNOT"
    print(compress(chaine))}

    La fonction devrait nous renvoyer :
    B{['T', 'O', 'B', 'E', 'O', 'R', 'N', 'O', 'T',
    256, 258, 260, 265, 259, 261, 263]}

    @param chaine: Chaine de caractère à compresser.

    @type chaine: C{string}

    @return: Cette fonction retourne une C{list}, correspondant aux
    caractères compressés.
    """
    taille_dico = 256
    dic = dict((chr(i), chr(i)) for i in range(0, taille_dico))

    w = ""
    res = []

    for c in chaine:
        wc = w+c
        if wc in dic:
            w = wc
        else:
            try:
                res.append(ord(dic[w]))
            except TypeError:
                res.append(dic[w])
            dic[wc] = taille_dico
            taille_dico = taille_dico + 1
            w = c

    if w:
        try:
            res.append(ord(dic[w]))
        except TypeError:
            res.append(dic[w])

    return res


def extAsciiUncompress(chaine):
    """
    Cette fonction va décompresser la valeur d'entrée. Cette valeur
    doit être une B{liste}.
    Il est possible de vérifier l'algorithme en ajoutant les lignes
    suivantes à la fonction I{main} de ce script :
    I{chaine = ['T', 'O', 'B', 'E', 'O', 'R', 'N', 'O', 'T',
    256, 258, 260, 265, 259, 261, 263]
    print(uncompress(chaine))}

    Cette fonction devrait renvoyer : B{TOBEORNOTTOBEORTOBEORNOT}

    @param chaine: C{list} à décompressée.

    @type chaine: C{list}

    @return: Cette fonction retourne la valeur décompressée en
    tant que C{string}.
    """
    # Initialize the dictionnary size (256 for ascii chars)
    # Creation of an ascii dictionnary
    taille_dico = 256
    maxi = taille_dico
    dic = dict((chr(i), chr(i)) for i in range(0, taille_dico))

    w = res = chaine.pop(0)
    for z in chaine:
        if z in dic and ord(z) >= taille_dico:
            inp = dic[z]
        elif ord(z) >= taille_dico and z not in dic:
            inp = w + w[0]
        else:
            inp = z
        res = res + inp

        dic[chr(maxi)] = w + inp[0]
        maxi += 1

        w = inp

    return res


def extAsciiCompFile(fileIn, fileOut):
    """
    La fonction compFile utilise la table ASCII étendue pour compresser.
    Cette technique se base sur 16 bits pour comprésser
    le fichier d'entrée I{fileIn}.
    Le fait d'utiliser la table ASCII étendue fait qu'on perd un peu en
    performance (la méthode demandée est    sur 9 bits), par contre,
     elle est bien plus simple à implémenter.

    @param fileIn: Fichier à compresser
    @param fileOut: Fichier de sortie, dans lequel sera mis le fichier
    compréssé.

    @type fileIn: C{list}
    @type fileOut: C{str}

    @return: C'est une procédure, il n'y a donc pas de valeur retournée.
    Cette procédure ne sert qu'à comprésser et rediriger le flux vers un
    fichier de sortie.
    """
    filename = fileIn
    fichier = open(filename, 'r')
    text = fichier.read()
    fichier.close()

    toto = extAsciiCompress(text)

    comp = ''.join([chr(item) for item in toto])

    a = open(fileOut, 'w+')
    a.write(comp)
    a.close()


def extAsciiDecompFile(fileIn, fileOut):
    """
    La fonction decompFile utilise la table ASCII étendue pour décompresser.
    Cette technique se base sur 16 bits pour décomprésser le
    fichier d'entrée I{fileIn}. Le fait d'utiliser la table ASCII étendue
    fait qu'on perd un peu en performance (la méthode demandée est sur 9 bits),
    par contre, elle est bien plus simple à implémenter.

    @param fileIn: Fichier à décompresser
    @param fileOut: Fichier de sortie, dans lequel sera mis le fichier
    décompréssé.

    @type fileIn: C{list}
    @type fileOut: C{str}

    @return: C'est une procédure, il n'y a donc pas de valeur retournée.
    Cette procédure ne sert qu'à comprésser et rediriger le flux vers un
    fichier de sortie.
    """
    filename = fileIn
    fichier = open(filename, 'r')
    text = fichier.read()
    fichier.close()

    liste = list(text)
    decomp = extAsciiUncompress(liste)

    fichier2 = open(fileOut, "w+")
    fichier2.write(decomp)
    fichier2.close()


def binaryCompress(unbinFileCompressedVar):
    """
    La fonction binaryCompress utilise la méthode binaire pour compresser.
    Elle va utiliser 9 bits pour compresser un fichier texte donné.
    Avec quelques tests, cette techniques est plus efficace et plus rapide
    que la méthode de l'ASCII. Mais plus compliquée à implémenter.

    @param unbinFileCompressedVar: Fichier à compresser

    @type unbinFileCompressedVar: C{str}

    @return: Cette fonction retourne une liste composée de C{str} et de C{int}.
    """

    dict_size = 256
    dictionary = dict((chr(i), chr(i)) for i in range(0, dict_size))

    w = ""
    result = []

    for c in unbinFileCompressedVar:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])

    ints = [el for el in result if isinstance(el, int)]

    bitlen = len(bin(max(ints))[2:])
    result.insert(0, bitlen)
    return result


def binaryDecompress(binFileCompressedVar):
    """
    Cette fonction va décompresser un fichier en entrée via l'algo LZW.

    @param binFileCompressedVar: Fichier à décompresser

    @type binFileCompressedVar: C{list}

    @return: Cette fonction retourne le fichier décompressé.
    """

    dict_size = 256
    dictionary = dict((chr(i), chr(i)) for i in range(0, dict_size))

    w = result = binFileCompressedVar.pop(0)
    for k in binFileCompressedVar:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad binFileCompressedVar k: %s' % k)
        result += entry

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result


def binaryFileCompress(binFilenameIn, binFilenameOut):
    """
    Cette fonction sert à compresser en binaire, il a été plus
    simple de le mettre dans une fonction à part.

    @param binFilenameIn: Fichier à compresser
    @param binFilenameOut: Fichier compressé après l'execution

    @type binFilenameIn: C{str}
    @type binFilenameOut: C{str}

    @return: Cette procédure ne fait qu'écrire le fichier
    compressé sur le disque, elle ne retourne rien.
    """
    with open(binFilenameIn, 'r') as file_in:
        raw_data = file_in.read()
        binFileCompressedVar_data = binaryCompress(raw_data)
        with open(binFilenameOut, 'wb') as f:
            binaryFileDump(binFileCompressedVar_data, f)


def binaryFileDeompress(binFilenameIn, binFilenameOut):
    """
    Cette fonction sert à décompresser en binaire, il a été plus
    simple de le mettre dans une fonction à part.

    @param binFilenameIn: Fichier à décompresser
    @param binFilenameOut: Fichier décompressé après l'execution

    @type binFilenameIn: C{str}
    @type binFilenameOut: C{str}

    @return: Cette procédure ne fait qu'écrire le fichier
    décompressé sur le disque, elle ne retourne rien.
    """
    with open(binFilenameOut, 'w+') as file_out:
        with open(binFilenameIn, 'rb') as f:
            binFileCompressedVar_data = binaryFileLoad(f)
        raw_data = binaryDecompress(binFileCompressedVar_data)
        file_out.write(raw_data)


def binaryFileWrite(binSeqFile, binCompFile):
    """
    Cette fonction va écrire un fichier niveau binaire.

    @param binSeqFile: Suite compressée
    @param binCompFile: Fichier compressé

    @type binSeqFile: C{int}
    @type binCompFile: C{str}

    @return: Cette procédure permet l'écriture d'un fichier binaire.
    Elle ne retourne donc rien.
    """
    bitlen = binSeqFile.pop(0)
    if bitlen > 255:
        raise ValueError("La taille du dictionnaire dépasse 2^255")

    binCompFile.write(bytearray([bitlen]))

    bits = ''
    for code in binSeqFile:
        b = bin(code)[2:]
        b = b.rjust(bitlen, '0')
        bits += b

    sio = StringIO(bits)
    byte = sio.read(8)
    while byte:
        byte = byte.ljust(8, '0')
        i = int(byte, 2)
        binCompFile.write(bytearray([i]))
        byte = sio.read(8)


def binaryFileRead(binCompFile):
    """
    Cette procédure permet d'extraire une suite de bits compressés
    et de les décompresser.

    @param binCompFile: Fichier compressé

    @type binCompFile: C{str}

    @return: Cette fonction retourne la suite de bits décompressé.
    """
    bits = ''

    bitlen = ord(binCompFile.read(1))
    byte = binCompFile.read(1)
    while byte:
        i = ord(byte)
        b = bin(i)[2:]
        b = b.rjust(8, '0')
        bits += b
        byte = binCompFile.read(1)

    binSeqFile = []
    sio = StringIO(bits)
    s = sio.read(bitlen)
    while s and len(s) == bitlen:
        binSeqFile.append(int(s, 2))
        s = sio.read(bitlen)
    return binSeqFile


def binaryFileDump(binSeqFile, binCompFile):
    """
    Cette procédure ne sert qu'à convertir tous les caractères en C{int}

    @param binSeqFile: Suite compressée
    @param binCompFile: Le fichier compressé

    @type binSeqFile: C{list}
    @type binCompFile: C{str}

    @return: Cette procédure ne sert qu'à la conversion. Elle ne retourne rien.
    """
    binSeqFile = [ord(el) if isinstance(el, str) else el for el in binSeqFile]
    binaryFileWrite(binSeqFile, binCompFile)


def binaryFileLoad(binCompFile):
    """
    Cette procédure ne sert qu'à convertir tous les C{int} en caractères

    @param binCompFile: Le fichier compressé

    @type binCompFile: C{str}

    @return: Cette procédure ne sert qu'à la conversion. Elle ne retourne rien.
    """
    binSeqFile = binaryFileRead(binCompFile)
    return [chr(el) if el <= 255 else el for el in binSeqFile]


if __name__ == '__main__':

    flag = True
    fileToCompress = "10000.txt"
    ASCIIDecomp = "genFiles/10000.ascii"
    binaryDecomp = "genFiles/10000.bin"
    output1 = "genFiles/10000.decompASCII"
    output2 = "genFiles/10000.decompBinary"

    while flag:
        try:
            print("LZW compressor / uncompressor\nChoose an action to perform")
            choice = int(input(" : \n[1] - Compress\n[2] - Uncompress\n> "))
            flag = False
        except ValueError:
            print("Must be an int. Do it again.")
            flag = True

        if not flag:
            if choice == 1:
                print("Bienvenue dans la compression de fichier.\n")
                start_timeASCII = time.time()
                extAsciiCompFile(fileToCompress, ASCIIDecomp)
                end_timeASCII = time.time() - start_timeASCII
                extAscii1 = os.stat(fileToCompress).st_size
                extAscii2 = os.stat(ASCIIDecomp).st_size
                tauxComp = 100 - ((extAscii2*100)/extAscii1)

                start_timeBinary = time.time()
                binaryFileCompress(fileToCompress, binaryDecomp)
                end_timeBinary = time.time() - start_timeBinary
                bin1 = os.stat(fileToCompress).st_size
                bin2 = os.stat(binaryDecomp).st_size
                tauxComp2 = 100 - ((bin2*100)/bin1)

                print("Extend ASCII method.")
                print("Le taux de compression est de : {0} %"
                      .format(round(tauxComp, 2)))
                print("Le fichier passe de : " +
                      str(os.stat(fileToCompress).st_size) +
                      " octets à : " + str(os.stat(ASCIIDecomp).st_size) +
                      " octets")
                print("La compression s'est faite en : {0} secondes\n"
                      .format(round(end_timeASCII, 4)))
                print("Binary method.")
                print("Le taux de compression est de : {0} %"
                      .format(round(tauxComp2, 2)))
                print("Le fichier passe de : " +
                      str(os.stat(fileToCompress).st_size) +
                      " octets à : " + str(os.stat(binaryDecomp).st_size) +
                      " octets")
                print("La compression s'est faite en : {0} secondes"
                      .format(round(end_timeBinary, 4)))
                flag = False
            elif choice == 2:
                print("Bienvenue dans la décompression de fichier.\n")
                extAsciiDecompFile(ASCIIDecomp, output1)
                binaryFileDeompress(binaryDecomp, output2)
                print("Extend ASCII method.")
                print("Le fichier {0} est décompréssé dans {1}\n"
                      .format(ASCIIDecomp, output1))
                print("Binary method.")
                print("Le fichier {0} est décompréssé dans {1}"
                      .format(binaryDecomp, output2))
                flag = False
            else:
                print("Bad choice. Do it again.")
                flag = True
