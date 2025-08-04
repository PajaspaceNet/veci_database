from flask import Flask, render_template_string, request, redirect, url_for
import psycopg2
import pandas as pd
import json

app = Flask(__name__)

db_config = {
    # doplň své přihlašovací údaje k DB
"dbname": "",
    "user": "",
    "password": "",
    "host": "",
    "port": 5432
}

def get_veci_table(order_by="co_to_je"):
    try:
        conn = psycopg2.connect(**db_config)
        query = f"""
            SELECT id, co_to_je, porcelan, cena, kde_je, krabice, pokoj, description, poznamka, prodat, tags, file_path, date_added, url
            FROM veci
            ORDER BY {order_by}
        """
        df = pd.read_sql_query(query, conn)
        if order_by == "kde_je":
            df = df.sort_values(by="kde_je", ascending=False)
        pocet_zaznamu = len(df)

        html_content = f"""
        <h1>Výstup z moji databaze veci</h1>
        <p>Počet záznamů: {pocet_zaznamu}</p>
        <table>
            <thead>
                <tr>
                    <th>Vybrat</th>
        """

        for col in df.columns:
            html_content += f"<th>{col}</th>"
        html_content += "<th>Akce</th>"
        html_content += "</tr></thead><tbody>"

        for row in df.itertuples(index=False):
            html_content += "<tr>"
            html_content += f'<td><input type="checkbox" onchange="toggleRowHighlight(this)"></td>'
            for i, value in enumerate(row):
                col_name = df.columns[i].lower()
                style = ""

                # Podmínky pro stylování buněk (můžeš upravit)
                if col_name == "co_to_je":
                    style = "background-color: #d9eaf7;"

                if col_name == "poznamka" and row.id == 42:
                    style += " background-color: #ffc0cb;"

                if col_name in ["url", "link", "website"] and value:
                    html_content += f'<td style="{style}"><a href="{value}" target="_blank">{value}</a></td>'
                else:
                    html_content += f'<td style="{style}">{value}</td>'

            # Tlačítko na smazání
            html_content += f"""
                <td>
                    <form method="post" action="/smazat/{row.id}" onsubmit="return confirm('Opravdu smazat?');">
                        <button type="submit">🗑️</button>
                    </form>
                </td>
            """
            html_content += "</tr>"

        html_content += "</tbody></table>"
        return html_content

    except Exception as e:
        return f"<p>Chyba při práci s databází: {e}</p>"

    finally:
        if 'conn' in locals():
            conn.close()

@app.route("/")
def index():
    veci_table = get_veci_table()
    page = f"""
    <html>
    <head>
        <title>Veci Dashboard</title>
        <style>
            table {{border-collapse: collapse; width: 100%;}}
            th, td {{border: 1px solid black; padding: 8px; text-align: left;}}
            th {{background-color: #f2f2f2; position: sticky; top: 0; z-index: 1;}}
            tr.selected {{background-color: #d0e7ff !important;}}
            button {{padding: 10px; margin: 5px;}}
        </style>
        <script>
            function toggleRowHighlight(checkbox) {{
                var row = checkbox.parentNode.parentNode;
                if (checkbox.checked) {{
                    row.classList.add('selected');
                }} else {{
                    row.classList.remove('selected');
                }}
            }}
        </script>
    </head>
    <body>
        <h1>Veci Aplikace</h1>
        <form method="get" action="/pridat" style="margin: 15px 0;">
          <button type="submit" style="font-size: 18px; padding: 10px 20px; cursor: pointer;">
            ➕ Přidat novou věc
          </button>
        </form>
        <form method="get" action="/">
            <button type="submit">🔄 Obnovit tabulku</button>
        </form>
        <form method="get" action="/serad_co_to_je">
            <button type="submit">📂 Seřadit podle CO_TO_JE</button>
        </form>
        <form method="get" action="/jina-sestava">
            <button type="submit">📊 Link na web autora - programatora </button>
        </form>
        {veci_table}
    </body>
    </html>
    """
    return render_template_string(page)

@app.route("/smazat/<int:id>", methods=["POST"])
def smazat(id):
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("DELETE FROM veci WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"<p>Chyba při mazání: {e}</p>"
    return redirect(url_for("index"))

@app.route("/serad_co_to_je")
def serad_co_to_je():
    veci_table = get_veci_table(order_by="co_to_je")
    page = f"""
    <html>
    <head>
        <title>Veci Dashboard - Seřazeno podle CO_TO_JE</title>
        <style>
            table {{border-collapse: collapse; width: 100%;}}
            th, td {{border: 1px solid black; padding: 8px; text-align: left;}}
            th {{background-color: #f2f2f2; position: sticky; top: 0; z-index: 1;}}
            tr.selected {{background-color: #d0e7ff !important;}}
            button {{padding: 10px; margin: 5px;}}
        </style>
        <script>
            function toggleRowHighlight(checkbox) {{
                var row = checkbox.parentNode.parentNode;
                if (checkbox.checked) {{
                    row.classList.add('selected');
                }} else {{
                    row.classList.remove('selected');
                }}
            }}
        </script>
    </head>
    <body>
        <h1>Moje Veci Aplikace - Seřazeno podle CO_TO_JE</h1>
        <form method="get" action="/">
            <button type="submit">🔄 Obnovit tabulku</button>
        </form>
        <form method="get" action="/serad_co_to_je">
            <button type="submit">📂 Seřadit podle CO_TO_JE</button>
        </form>
        <form method="get" action="/jina-sestava">
            <button type="submit">📊 link na pavlusa.com</button>
        </form>
        {veci_table}
    </body>
    </html>
    """
    return render_template_string(page)

@app.route("/jina-sestava")
def jina_sestava():
    return "<h2>linky na jine sestavy ,nyni vedou na autoruv web</h2><p><a href='https://www.pavlusa.com'>tudy se dostanes na web autora :-)</a></p>"

@app.route("/pridat", methods=["GET", "POST"])
def pridat():
    if request.method == "POST":
        co_to_je = request.form.get("co_to_je")
        porcelan = True if request.form.get("porcelan") == "1" else False
        cena = request.form.get("cena")
        kde_je = request.form.get("kde_je")
        krabice = request.form.get("krabice")
        pokoj = request.form.get("pokoj")
        description = request.form.get("description")
        poznamka = request.form.get("poznamka")
        prodat = request.form.get("prodat")
        tags = request.form.get("tags")
        file_path = request.form.get("file_path")
        url = request.form.get("url")

        # Detail porcelánu
        znacka = request.form.get("znacka")
        rozmer = request.form.get("rozmer")
        stav = request.form.get("stav")
        zajimavost = request.form.get("zajimavost")

        foto_vady_raw = request.form.get(
            "foto_vady_input")  # tahle hodnota je čistý text z formuláře, např. "prasklina, škrábanec"
        if foto_vady_raw:
            foto_vady = [v.strip() for v in foto_vady_raw.split(",") if v.strip()]  # převede na list stringů
        else:
            foto_vady = []

        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO veci (co_to_je, porcelan, cena, kde_je, krabice, pokoj, description, poznamka, prodat, tags, file_path, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (co_to_je, porcelan, cena, kde_je, krabice, pokoj, description, poznamka, prodat, tags, file_path, url))
            vec_id = cur.fetchone()[0]

            if porcelan:
                cur.execute("""
                    INSERT INTO porcelan_info (vec_id, znacka, rozmer, stav, zajimavost, foto_vady)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (vec_id, znacka, rozmer, stav, zajimavost, foto_vady))

            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("index"))

        except Exception as e:
            return f"<h3>Chyba při vkládání do databáze:</h3><pre>{e}</pre>"

    # GET zobraz formulář
    form_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Přidat novou věc</title>
        <style>
            label {display: block; margin: 8px 0 4px;}
            input[type=text], textarea {width: 100%; padding: 6px; box-sizing: border-box;}
            #porcelan_detail {display: none; border: 1px solid #ccc; padding: 10px; margin-top: 10px;}
            button {margin-top: 12px; padding: 10px 15px;}
            body {max-width: 600px; margin: 20px auto; font-family: Arial, sans-serif;}
        </style>
        <script>
            function togglePorcelan() {
                var c = document.getElementById('porcelan');
                var d = document.getElementById('porcelan_detail');
                d.style.display = c.checked ? 'block' : 'none';
            }

            function updateFotoVady() {
                var input = document.getElementById('foto_vady_input').value;
                var arr = input.split(',').map(s => s.trim()).filter(s => s.length > 0);
                document.getElementById('foto_vady').value = JSON.stringify(arr);
            }

            window.onload = function() {
                togglePorcelan();
                document.getElementById('foto_vady_input').addEventListener('change', updateFotoVady);
            }
        </script>
    </head>
    <body>
        <h1>Přidat novou věc</h1>
        <form method="post">
            <label>Co to je:<input type="text" name="co_to_je" required></label>
            <label><input type="checkbox" id="porcelan" name="porcelan" value="1" onchange="togglePorcelan()"> Porcelán</label>
            <label>Cena:<input type="text" name="cena"></label>
            <label>Kde je:<input type="text" name="kde_je"></label>
            <label>Krabice:<input type="text" name="krabice"></label>
            <label>Pokoj:<input type="text" name="pokoj"></label>
            <label>Description:<textarea name="description"></textarea></label>
            <label>Poznámka:<textarea name="poznamka"></textarea></label>
            <label>Prodat:<input type="text" name="prodat"></label>
            <label>Tags:<input type="text" name="tags"></label>
            <label>File Path:<input type="text" name="file_path"></label>
            <label>URL:<input type="text" name="url"></label>

            <div id="porcelan_detail">
                <h3>Detaily porcelánu</h3>
                <label>Značka a původ:<input type="text" name="znacka"></label>
                <label>Rozměry:<input type="text" name="rozmer"></label>
                <label>Stav:<input type="text" name="stav"></label>
                <label>Zajímavost:<textarea name="zajimavost"></textarea></label>
                <label>Foto vady (oddělené čárkou):<input type="text" id="foto_vady_input" name="foto_vady_input"></label>
               
            </div>

            <button type="submit">Uložit</button>
        </form>
        <p><a href="/">⬅ Zpět na přehled</a></p>
    </body>
    </html>
    """
    return render_template_string(form_html)

if __name__ == "__main__":
    app.run(debug=True, port=5009)
