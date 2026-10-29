from html import escape

import resend
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

resend.api_key = os.environ.get("RESEND_API_KEY", "")
resend_sender = os.environ.get("RECEIVER", "tsilavinaraz07@gmail.com")

def format_ariary(montant):
    """Formate un montant : 1234567 -> '1 234 567 Ar'"""
    try:
        return f"{round(float(montant or 0)):,}".replace(",", " ") + " Ar"
    except (TypeError, ValueError):
        return "0 Ar"


@api_view(["POST"])
def send_devis_email(request):
    nom = escape(str(request.data.get("nom") or ""))
    email = escape(str(request.data.get("email") or ""))
    telephone = escape(str(request.data.get("telephone") or ""))
    adresse = escape(str(request.data.get("adresse") or ""))
    devis = request.data.get("devis") or {}

    # Les lignes du devis contiennent déjà : taillePack, prixPack, totalPieces,
    # totalHT, montantTVA, totalTTC (calculés côté frontend).
    lignes = devis.get("lignes") or []

    produits_html = ""
    for ligne in lignes:
        taille_pack = ligne.get("taillePack")
        quantite = ligne.get("quantite", 0)

        if taille_pack:
            type_vente = f"Pack de {taille_pack} pièces"
            quantite_txt = f"{quantite} pack(s)"
        else:
            type_vente = "À l'unité"
            quantite_txt = f"{quantite}"

        produits_html += f"""
            <tr>
                <td style="padding:10px;border:1px solid #e2e8f0;">
                    <strong>{escape(str(ligne.get("name", "")))}</strong><br>
                    <span style="color:#64748b;font-size:12px;">{type_vente}</span>
                </td>
                <td style="padding:10px;border:1px solid #e2e8f0;text-align:center;">{quantite_txt}</td>
                <td style="padding:10px;border:1px solid #e2e8f0;text-align:center;">{ligne.get("totalPieces", quantite)}</td>
                <td style="padding:10px;border:1px solid #e2e8f0;text-align:right;">{format_ariary(ligne.get("prixPack"))}</td>
                <td style="padding:10px;border:1px solid #e2e8f0;text-align:right;">{format_ariary(ligne.get("totalHT"))}</td>
                <td style="padding:10px;border:1px solid #e2e8f0;text-align:right;">{format_ariary(ligne.get("montantTVA"))}</td>
                <td style="padding:10px;border:1px solid #e2e8f0;text-align:right;"><strong>{format_ariary(ligne.get("totalTTC"))}</strong></td>
            </tr>
        """

    resend.Emails.send(
        {
            "from": "Sainto Madagascar <onboarding@resend.dev>",
            # Ici tu peux envoyer au client
            "to": f"{resend_sender}",
            "subject": f"Confirmation du commande de {email}",
            "html": f"""
            <div style="font-family:Arial,sans-serif;color:#0f172a;max-width:760px;">

                <h2 style="color:#2563eb;">Devis / Commande Sainto Madagascar</h2>
                <p style="color:#64748b;">Émis le {escape(str(devis.get("date", "")))}</p>

                <div style="background:#fffbeb;border-left:4px solid #f59e0b;padding:12px 16px;margin:16px 0;">
                    <strong>NOTE IMPORTANTE :</strong> nous ne vendons que par pack
                    les produits Sainto (1,5 L, 1 L, 0,5 L) et Ice Tea.<br>
                    Sainto 1,5 L, Sainto 1 L et Ice Tea 1,5 L : <strong>6 pièces</strong> par pack.<br>
                    Sainto 0,5 L et Ice Tea 0,5 L : <strong>8 pièces</strong> par pack.
                </div>

                <h2>Informations du client</h2>
                <p><strong>Nom :</strong> {nom}</p>
                <p><strong>Email :</strong> {email}</p>
                <p><strong>Téléphone :</strong> {telephone}</p>
                <p><strong>Adresse :</strong> {adresse}</p>

                <h2>Produits commandés</h2>

                <table style="border-collapse:collapse;width:100%;font-size:13px;">
                    <tr style="background:#eff6ff;">
                        <th style="padding:10px;border:1px solid #e2e8f0;text-align:left;">Produit</th>
                        <th style="padding:10px;border:1px solid #e2e8f0;">Quantité</th>
                        <th style="padding:10px;border:1px solid #e2e8f0;">Total pièces</th>
                        <th style="padding:10px;border:1px solid #e2e8f0;">Prix du pack (TTC)</th>
                        <th style="padding:10px;border:1px solid #e2e8f0;">HT</th>
                        <th style="padding:10px;border:1px solid #e2e8f0;">TVA</th>
                        <th style="padding:10px;border:1px solid #e2e8f0;">TTC</th>
                    </tr>
                    {produits_html}
                </table>

                <h2>Résumé</h2>
                <p><strong>Total pièces :</strong> {devis.get("totalPieces", "")}</p>
                <p><strong>Total HT :</strong> {format_ariary(devis.get("totalHT"))}</p>
                <p><strong>TVA :</strong> {format_ariary(devis.get("totalTVA"))}</p>
                <p style="font-size:18px;color:#1d4ed8;">
                    <strong>Total TTC : {format_ariary(devis.get("totalTTC"))}</strong>
                </p>

                <br>

                <p>
                    Merci de votre confiance.<br>
                    <strong>Sainto Madagascar 💧</strong>
                </p>
            </div>
        """,
        }
    )

    return Response({"success": True, "message": "Email envoyé"})