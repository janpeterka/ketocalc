"""empty message

Revision ID: 5dd92f141282
Revises: 118f7bcd451b
Create Date: 2020-04-30 16:16:43.075213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5dd92f141282"
down_revision = "118f7bcd451b"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        INSERT INTO ingredients(name,calorie,fat,sugar,protein,is_shared,is_approved,source,author,created) VALUES
            ('Ananas',212,0.2,10.6,0.5,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Angrešt',186,0.2,8.3,0.8,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Artyčok',261,0.6,5.5,3.2,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Avokádo',697,16.5,1.4,1.5,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Banány',415,0.3,21.6,1.1,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Brokolice',153,0.3,2,4.4,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Broskve',205,0.2,10,0.9,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Celer bulvový',117,0.3,2.6,1.5,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Celer řapíkatý',69,0.2,0.7,0.7,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Cibule',164,0.3,6.6,1.4,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Cibule červená',191,0.2,8.6,1.4,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Citróny',149,0.4,6.1,0.7,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Cuketa',57,0.1,1.8,0.8,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Cukr řepný, bílý',1700,0,99.8,0,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Cukr třtinový',1680,0,98.9,0,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Česnek',636,0.4,28.9,6.3,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Dýně, Hokkaidó',154,0.6,5.7,1.1,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Grapefruit',170,0.2,8.2,0.6,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Hrušky',238,0.3,11.3,0.5,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Jablka',219,0.4,10.5,0.4,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Jahody zahradní',158,0.4,6.7,0.8,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Kapusta růžičková',204,0.5,4.5,4.5,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Kiwi',244,0.8,10.3,1,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Koření nové',1430,7,53.2,5.6,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Koření, hřebíček',1510,17.2,29,5.8,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Koření, kardamom',1138,2,35.9,8.6,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Koření, kmín',1360,13.7,19.5,12.6,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Koření, kurkuma',1296,1.7,53.2,9.5,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Koření, majoránka, sušená',1090,5.6,18.6,14.3,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Koření, paprika, sladká, mletá',1344,13.8,13.7,15,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Koření, pepř, černý',1400,8.6,42.5,11.8,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Květák',110,0.2,2.5,2.4,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Lilek',77,0,2.8,0.8,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Limetka',148,0,6.6,0.6,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Maliny',209,0.6,6.8,1.2,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Mandarinky',176,0.2,8.9,0.6,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Mango',292,0.5,14.7,0.6,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Meruňky',223,0.1,11.2,0.5,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Mrkev',151,0.2,6.1,1,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Nektarinky',200,0.3,9.3,1.1,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Okurky',48,0.1,1.5,0.8,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Ořechy lískové',2724,61.4,4.2,14.4,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Ořechy vlašské',2740,61.2,6.6,16.3,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Ostružiny',225,1,7,1.4,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Pažitka',131,0.7,2.7,2.4,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Polníček',79,0.4,0.5,2.2,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Pomelo',170,0.1,8.4,0.9,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Pomeranče',209,0.2,10,0.9,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Pórek',136,0.3,3.8,2.2,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Rajčata',88,0.2,3.1,0.9,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Rebarbora',63,0,1.5,0.9,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Rukola',74,0.3,0,2.7,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Rybíz bílý',218,1.1,6.2,1.1,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Rybíz černý',258,0.3,10.6,1.2,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Rybíz červený',205,0.2,8,1.1,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Ředkvička',45,0,1.6,0.6,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Řepa červená',166,0.2,7.2,1.3,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Salát hlávkový',65,0.2,1.4,1.3,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Skořice mletá',973,1.9,21.3,3.8,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Sůl jedlá',0,0,0,0,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Švestky',250,0.2,12.4,0.7,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Vejce slepičí',575,9.2,1.3,12.5,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Víno - hrozny',302,0.4,15.2,0.7,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Višně',234,0.5,10.9,1,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Zázvor',115,0.2,3.9,1.1,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00'),
            ('Žampiony',98,0.3,1.4,2.9,1,0,'nutridatabaze','admin', '2020-04-30 14:30:00')
        """
    )
    pass


def downgrade():
    pass
