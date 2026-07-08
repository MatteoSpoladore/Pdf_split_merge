# from PIL import Image


# def converti_in_bianco(input_path, output_path):
#     # Apri l'immagine e assicurati che abbia il canale Alpha (RGBA)
#     img = Image.open(input_path).convert("RGBA")

#     # Separa i canali (Rosso, Verde, Blu, Trasparenza)
#     _, _, _, alpha = img.split()

#     # Crea una nuova immagine completamente bianca della stessa dimensione
#     img_bianca = Image.new("RGBA", img.size, (255, 255, 255, 255))

#     # Applica la trasparenza originale all'immagine bianca
#     img_bianca.putalpha(alpha)

#     # Salva il risultato
#     img_bianca.save(output_path, format="svg")
#     print(f"Fatto! Icona salvata come: {output_path}")


# if __name__ == "__main__":
#     # Inserisci qui il nome del tuo file originale e come vuoi chiamare il nuovo
#     converti_in_bianco("icon.svg", "icona_bianca.svg")

import xml.etree.ElementTree as ET


def converti_svg_in_bianco(input_path, output_path):
    # Evita che Python aggiunga prefissi strani come "ns0:" ai tag SVG
    ET.register_namespace("", "http://www.w3.org/2000/svg")

    try:
        tree = ET.parse(input_path)
        root = tree.getroot()

        # Imposta il colore di default del contenitore principale su bianco
        root.attrib["fill"] = "#FFFFFF"

        # Passa in rassegna tutti i nodi (path, cerchi, rettangoli, ecc.)
        for elem in root.iter():
            # Se l'elemento ha un 'fill' (riempimento) che non è trasparente, fallo bianco
            if elem.get("fill") not in [None, "none"]:
                elem.set("fill", "#FFFFFF")

            # Se l'elemento ha un 'stroke' (bordo) che non è trasparente, fallo bianco
            if elem.get("stroke") not in [None, "none"]:
                elem.set("stroke", "#FFFFFF")

        # Salva il nuovo file SVG
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print(f"Fatto! Icona SVG salvata come: {output_path}")

    except Exception as e:
        print(f"Errore durante l'elaborazione del file: {e}")


if __name__ == "__main__":
    converti_svg_in_bianco("icon.svg", "icona_bianca.svg")
