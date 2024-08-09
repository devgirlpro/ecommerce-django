from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db import connection
from .models import Customer, Product, Order


def execute_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

def customers_with_orders(request):
    query = """
        SELECT DISTINCT c.first_name, c.last_name
        FROM store_customer c
        JOIN store_order o ON c.id = o.customer_id;
    """
    customers = execute_query(query)
    return render(request, 'store/customers_with_orders.html', {'customers': customers})

def customer_revenue(request):
    query = """
        SELECT c.first_name, c.last_name, COUNT(o.id) AS total_orders, COALESCE(SUM(oi.quantity * oi.price), 0) AS total_revenue
        FROM store_customer c
        LEFT JOIN store_order o ON c.id = o.customer_id
        LEFT JOIN store_orderitem oi ON o.id = oi.order_id
        GROUP BY c.id;
    """
    customers = execute_query(query)
    return render(request, 'store/customer_revenue.html', {'customers': customers})

def best_selling_products(request):
    query = """
        SELECT 
            p.id AS product_id, 
            p.name AS product_name, 
            COUNT(DISTINCT oi.order_id) AS order_count, 
            SUM(oi.quantity) AS total_quantity_ordered,
            GROUP_CONCAT(DISTINCT CONCAT(c.first_name, ' ', c.last_name)) AS customers
        FROM store_product p
        JOIN store_orderitem oi ON p.id = oi.product_id
        JOIN store_order o ON oi.order_id = o.id
        JOIN store_customer c ON o.customer_id = c.id
        GROUP BY p.id, p.name
        ORDER BY order_count DESC;
    """
    products = execute_query(query)
    return render(request, 'store/best_selling_products.html', {'products': products})


def high_spending_customers(request):
    query = """
        SELECT CONCAT(c.first_name, ' ', c.last_name) AS full_name, COALESCE(SUM(oi.quantity * oi.price), 0) AS total_spent
        FROM store_customer c
        LEFT JOIN store_order o ON c.id = o.customer_id
        LEFT JOIN store_orderitem oi ON o.id = oi.order_id
        GROUP BY c.id
        HAVING total_spent > 40
        ORDER BY total_spent DESC;
    """
    customers = execute_query(query)
    return render(request, 'store/high_spending_customers.html', {'customers': customers})



def home(request):
    return render(request, 'store/home.html')

def customer_overview(request):
    customers = Customer.objects.all()
    for customer in customers:
        customer.order_count = Order.objects.filter(customer=customer).count()
    return render(request, 'store/customers.html', {'customers': customers})

def product_overview(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})

def order_details(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = Order.objects.filter(customer=customer)
    total_amount = sum(order.total_amount for order in orders)
    return render(request, 'store/order_details.html', {'customer': customer, 'orders': orders, 'total_amount': total_amount})

from django.shortcuts import render

def questions(request):
    return render(request, 'store/questions.html')

def questions_detail(request, section):
    sections = {
        'general_database_questions': 'General Database Questions',
        'sql_database_queries': 'SQL and Database Queries',
        'database_design_architecture': 'Database Design and Architecture'
    }
    
    questions_and_answers = {
        'general_database_questions': [
            {
                'question': "1- Welche Unterschiede sehen Sie zwischen relationalen und nicht-relationalen Datenbanken?",
                'answer': (
                    "Relationale Datenbanken:\n\n"
                    "Struktur und Organisation:\n\n"
                    "Relationale Datenbanken sind in Tabellen organisiert, die aus Zeilen und Spalten bestehen. "
                    "Jede Tabelle repräsentiert eine Entität (z.B. Kunden, Produkte), und jede Zeile in einer Tabelle "
                    "stellt einen Datensatz dar. Die Spalten definieren die Attribute dieser Entität (z.B. Name, Preis, Adresse).\n\n"
                    "Schema und Datenintegrität:\n\n"
                    "Relationale Datenbanken verwenden ein festes Schema, das vor der Speicherung der Daten definiert wird. "
                    "Dieses Schema stellt sicher, dass die Datenstruktur konstant bleibt und alle Daten die definierten Regeln und "
                    "Beschränkungen einhalten, wie z.B. Datentypen und Schlüsselintegrität (Primary Keys, Foreign Keys). "
                    "Die Datenintegrität wird durch Constraints (z.B. NOT NULL, UNIQUE, FOREIGN KEY) gewährleistet, die sicherstellen, "
                    "dass die Daten korrekt und konsistent bleiben.\n\n"
                    "Beziehungen:\n\n"
                    "Die Stärke relationaler Datenbanken liegt in ihrer Fähigkeit, Beziehungen zwischen Tabellen zu definieren und "
                    "zu verwalten. Diese Beziehungen werden durch Schlüssel (Primary Keys und Foreign Keys) hergestellt und ermöglichen es, "
                    "komplexe Abfragen über mehrere Tabellen hinweg durchzuführen. Zum Beispiel kann eine Bestellung in einer E-Commerce-Datenbank "
                    "mit einem Kunden und den bestellten Produkten über Foreign Keys verknüpft werden.\n\n"
                    "Transaktionen und ACID-Eigenschaften:\n\n"
                    "Relationale Datenbanken unterstützen Transaktionen, die die ACID-Eigenschaften (Atomicity, Consistency, Isolation, Durability) "
                    "garantieren. Dies bedeutet, dass alle Operationen innerhalb einer Transaktion entweder vollständig ausgeführt oder vollständig "
                    "rückgängig gemacht werden, um die Datenintegrität zu gewährleisten.\n\n"
                    "Anwendungsbeispiele:\n\n"
                    "Typische Anwendungen relationaler Datenbanken sind Finanzsysteme, Buchhaltungssoftware, E-Commerce-Plattformen und alle Systeme, "
                    "die eine strenge Datenintegrität und komplexe Abfragen erfordern. Beispiele für relationale Datenbanken: MySQL, PostgreSQL, Oracle, "
                    "Microsoft SQL Server.\n\n"
                    "Nicht-relationale Datenbanken (NoSQL):\n\n"
                    "Struktur und Flexibilität:\n\n"
                    "Nicht-relationale Datenbanken (auch NoSQL-Datenbanken genannt) haben eine flexible Struktur und verwenden verschiedene Datenmodelle "
                    "wie Dokumentenorientierte, Schlüssel-Wert-, Spaltenbasierte und Graphdatenbanken. Diese Datenbanken sind schemalos oder verwenden "
                    "ein dynamisches Schema, das sich zur Laufzeit ändern kann. Dies ermöglicht es, unstrukturierte oder halbstrukturierte Daten zu speichern, "
                    "ohne ein starres Schema einhalten zu müssen.\n\n"
                    "Datenmodelle:\n\n"
                    "Dokumentenorientiert: Daten werden als Dokumente (z.B. JSON, BSON) gespeichert. Jedes Dokument kann unterschiedlich strukturierte Daten enthalten. "
                    "Beispiel: MongoDB.\n\n"
                    "Schlüssel-Wert: Daten werden als einfache Schlüssel-Wert-Paare gespeichert, ähnlich wie in einem Wörterbuch. Beispiel: Redis.\n\n"
                    "Spaltenbasiert: Daten werden in Spaltenfamilien organisiert, die effizient für bestimmte Arten von Abfragen und Big Data geeignet sind. "
                    "Beispiel: Apache Cassandra.\n\n"
                    "Graph: Daten werden als Knoten und Kanten gespeichert, ideal für stark vernetzte Daten wie soziale Netzwerke. Beispiel: Neo4j.\n\n"
                    "Skalierbarkeit und Leistung:\n\n"
                    "NoSQL-Datenbanken bieten eine hohe horizontale Skalierbarkeit, was bedeutet, dass sie einfach über mehrere Server hinweg skaliert werden können, "
                    "um große Datenmengen und hohe Transaktionsvolumina zu verarbeiten. Sie sind oft für schnelle Lese- und Schreiboperationen optimiert und eignen sich "
                    "gut für Anwendungen mit variablen und sich schnell ändernden Datenstrukturen.\n\n"
                    "Verzicht auf ACID in einigen Fällen:\n\n"
                    "Im Gegensatz zu relationalen Datenbanken verzichten einige NoSQL-Datenbanken auf strikte ACID-Eigenschaften zugunsten von BASE-Eigenschaften "
                    "(Basically Available, Soft state, Eventually consistent), um eine bessere Skalierbarkeit und Verfügbarkeit zu erreichen.\n\n"
                    "Anwendungsbeispiele:\n\n"
                    "NoSQL-Datenbanken werden häufig in modernen Webanwendungen, Echtzeitanalysen, Big Data, Content Management Systemen und Anwendungen eingesetzt, "
                    "die flexible Datenmodelle und eine hohe Skalierbarkeit erfordern. Beispiele für NoSQL-Datenbanken: MongoDB, Cassandra, Redis, Neo4j.\n\n"
                    "Zusammenfassung:\n\n"
                    "Relationale Datenbanken sind ideal für Anwendungen, die eine starke Datenintegrität, festes Schema und komplexe Abfragen benötigen. Sie eignen sich "
                    "für strukturierte Daten und Anwendungen, bei denen Konsistenz und Transaktionssicherheit entscheidend sind. Nicht-relationale Datenbanken bieten "
                    "Flexibilität und Skalierbarkeit und sind ideal für unstrukturierte Daten und Anwendungen, die schnelle Lese- und Schreibzugriffe sowie variable "
                    "Datenmodelle erfordern."
                )
            },
            {
                'question': "2- Unter welchen Umständen würden Sie eine relationale Datenbank gegenüber einer nicht-relationalen bevorzugen?",
                'answer': (
                    "Datenintegrität und Konsistenz:\n\n"
                    "Wenn Ihre Anwendung eine strikte Datenintegrität und Konsistenz erfordert, sind relationale Datenbanken zu bevorzugen, da sie ACID-Eigenschaften "
                    "(Atomicity, Consistency, Isolation, Durability) gewährleisten. Dies stellt sicher, dass Transaktionen zuverlässig verarbeitet werden und die Datenbank "
                    "in einem konsistenten Zustand bleibt.\n\n"
                    "Beispiel: Finanzanwendungen, bei denen genaue und konsistente Transaktionen entscheidend sind, wie z.B. Bankensysteme und Buchhaltungssoftware.\n\n"
                    "Komplexe Abfragen und Transaktionen:\n\n"
                    "Wenn Ihre Anwendung komplexe Abfragen und Transaktionen erfordert, die mehrere Tabellen umfassen, sind relationale Datenbanken ideal. SQL, die Abfragesprache "
                    "für relationale Datenbanken, ist leistungsstark und gut geeignet für komplexe Joins und Aggregationen.\n\n"
                    "Beispiel: E-Commerce-Plattformen, bei denen detaillierte Berichte über Kundenbestellungen, Produktbestände und Verkaufsanalysen erstellt werden müssen.\n\n"
                    "Strukturierte Daten:\n\n"
                    "Wenn die Daten hochstrukturiert sind und die Beziehungen zwischen den verschiedenen Entitäten gut definiert sind, sind relationale Datenbanken eine natürliche Wahl. "
                    "Sie verwenden ein festes Schema, das die Datenkonsistenz und -integrität sicherstellt.\n\n"
                    "Beispiel: Customer Relationship Management (CRM)-Systeme, bei denen Kundendaten, Interaktionen und Transaktionen strukturiert und miteinander verknüpft sein müssen.\n\n"
                    "Datensicherheit:\n\n"
                    "Relationale Datenbanken bieten robuste Sicherheitsfunktionen wie Benutzerauthentifizierung, Autorisierung und Zugriffskontrollen. Dies ist entscheidend für Anwendungen, "
                    "die mit sensiblen Daten umgehen.\n\n"
                    "Beispiel: Gesundheitssysteme, bei denen Patientendaten sicher gespeichert und nur von autorisiertem Personal abgerufen werden dürfen.\n\n"
                    "Standardisierung und Compliance:\n\n"
                    "Wenn Sie branchenspezifische Standards und regulatorische Anforderungen erfüllen müssen, sind relationale Datenbanken oft die bevorzugte Wahl, da sie Funktionen bieten, "
                    "die bei der Einhaltung dieser Anforderungen helfen.\n\n"
                    "Beispiel: Anwendungen im Finanzsektor, die den Vorschriften wie GDPR, HIPAA oder SOX entsprechen müssen.\n\n"
                    "Reife Ökosystem und Tools:\n\n"
                    "Relationale Datenbanken haben ein reifes Ökosystem mit einer Vielzahl von Tools für Backup, Wiederherstellung, Leistungsoptimierung und Überwachung. Dies erleichtert "
                    "ihre Verwaltung und Wartung.\n\n"
                    "Beispiel: Enterprise Resource Planning (ERP)-Systeme, bei denen robuste Datenbankverwaltungswerkzeuge erforderlich sind, um einen reibungslosen Betrieb zu gewährleisten."
                )
            },
            {
                'question': "3- Können Sie mir die ACID-Eigenschaften erklären und warum diese in Datenbanken wichtig sind?",
                'answer': (
                    "Atomicity (Atomarität):\n\n"
                    "Beschreibung: Die Atomarität stellt sicher, dass alle Operationen innerhalb einer Transaktion als eine einzige, unteilbare Einheit betrachtet werden. "
                    "Das bedeutet, dass entweder alle Operationen erfolgreich abgeschlossen werden oder keine. Wenn eine Operation in einer Transaktion fehlschlägt, werden "
                    "alle vorherigen Operationen rückgängig gemacht.\n\n"
                    "Beispiel: Stellen Sie sich eine Banküberweisung vor. Wenn das Geld vom Konto des Absenders abgebucht, aber nicht auf das Konto des Empfängers gutgeschrieben wird, "
                    "führt die Atomarität dazu, dass die gesamte Transaktion rückgängig gemacht wird, um Inkonsistenzen zu vermeiden.\n\n"
                    "Consistency (Konsistenz):\n\n"
                    "Beschreibung: Konsistenz bedeutet, dass eine Transaktion das Datenbanksystem von einem konsistenten Zustand in einen anderen konsistenten Zustand überführt. "
                    "Alle definierten Regeln, wie Constraints, Trigger und Validierungen, müssen während der Transaktion eingehalten werden.\n\n"
                    "Beispiel: Bei einer Produktbestellung müssen alle Bedingungen erfüllt sein, wie die Verfügbarkeit des Produkts und die Gültigkeit der Kreditkartendaten, bevor "
                    "die Bestellung als erfolgreich betrachtet wird.\n\n"
                    "Isolation (Isolation):\n\n"
                    "Beschreibung: Die Isolation stellt sicher, dass parallele Transaktionen sich nicht gegenseitig beeinflussen. Jede Transaktion sollte so ausgeführt werden, als ob sie "
                    "die einzige im System ist. Dies verhindert Inkonsistenzen durch gleichzeitig ablaufende Transaktionen.\n\n"
                    "Beispiel: Wenn zwei Kunden gleichzeitig denselben Artikel kaufen, sorgt die Isolation dafür, dass die Transaktionen nacheinander verarbeitet werden, um sicherzustellen, "
                    "dass der Artikel nicht zweimal verkauft wird.\n\n"
                    "Durability (Dauerhaftigkeit):\n\n"
                    "Beschreibung: Dauerhaftigkeit garantiert, dass einmal bestätigte Transaktionen auch bei Systemausfällen oder Abstürzen dauerhaft gespeichert bleiben. "
                    "Die Änderungen werden auf nichtflüchtigen Speicher (z.B. Festplatten) geschrieben.\n\n"
                    "Beispiel: Nach Abschluss einer Flugbuchung bleibt die Buchung auch bei einem Stromausfall oder Systemabsturz erhalten und geht nicht verloren.\n\n"
                    "Bedeutung der ACID-Eigenschaften in Datenbanken:\n\n"
                    "Datenintegrität: Die ACID-Eigenschaften gewährleisten, dass Daten korrekt, konsistent und zuverlässig gespeichert werden, was für die Datenintegrität entscheidend ist.\n\n"
                    "Fehlertoleranz: Durch die Sicherstellung, dass Transaktionen entweder vollständig oder gar nicht ausgeführt werden, können Systeme Fehler und Abstürze besser tolerieren, "
                    "ohne die Konsistenz der Daten zu gefährden.\n\n"
                    "Parallelität: Die Isolation ermöglicht es, dass mehrere Transaktionen gleichzeitig ohne Konflikte oder Inkonsistenzen ausgeführt werden können.\n\n"
                    "Verlässlichkeit: Die Dauerhaftigkeit sorgt dafür, dass bestätigte Daten auch langfristig erhalten bleiben, was besonders in kritischen Anwendungen wichtig ist."
                )
            },
            {
                'question': "4- Was verstehen Sie unter dem Konzept der Normalisierung, und wann halten Sie eine Denormalisierung für sinnvoll?",
                 'answer': (
                    "Normalisierung:\n\n"
                    "Beschreibung: Normalisierung ist ein Prozess in der Datenbankgestaltung, der darauf abzielt, Datenredundanzen zu minimieren und Datenintegrität zu gewährleisten. "
                    "Dieser Prozess teilt große Tabellen in kleinere, miteinander verknüpfte Tabellen auf, um sicherzustellen, dass jede Dateninformation nur einmal gespeichert wird.\n\n"
                    "Beispiel: Stellen Sie sich eine Tabelle vor, die Informationen über Kunden und ihre Bestellungen enthält. Ohne Normalisierung könnten Kundendaten wie Name und Adresse "
                    "für jede Bestellung wiederholt werden. Durch Normalisierung würden diese Daten in separate Tabellen aufgeteilt: eine für die Kundeninformationen und eine andere für die "
                    "Bestelldetails. Dadurch wird sichergestellt, dass jede Information nur einmal gespeichert wird und leicht aktualisiert werden kann.\n\n"
                    "Vorteile der Normalisierung:\n\n"
                    "Reduzierung von Datenredundanz: Verhindert, dass dieselben Daten mehrfach gespeichert werden, was Speicherplatz spart und die Konsistenz erhöht.\n\n"
                    "Verbesserung der Datenintegrität: Durch die Minimierung von Redundanzen verringert sich das Risiko von Inkonsistenzen. Änderungen an den Daten müssen nur an einer Stelle vorgenommen werden.\n\n"
                    "Einfachere Wartung: Wenn die Datenstruktur gut organisiert ist, wird die Datenbank leichter wartbar und erweiterbar.\n\n"
                    "Denormalisierung:\n\n"
                    "Beschreibung: Denormalisierung ist das Gegenteil der Normalisierung. Es ist der Prozess, bei dem bewusst Redundanzen in eine Datenbank eingeführt werden, um die Leistung zu verbessern, "
                    "insbesondere bei Leseoperationen. Denormalisierung bedeutet, dass Daten, die normalerweise getrennt gehalten werden, zusammengeführt werden, um die Anzahl der benötigten Joins zu reduzieren.\n\n"
                    "Beispiel: In einem Reporting-System, das häufige Abfragen nach dem Verkaufsvolumen pro Kunde ausführt, könnte es sinnvoll sein, eine denormalisierte Tabelle zu erstellen, die sowohl die "
                    "Kundendaten als auch die Verkaufsdaten enthält. Dies reduziert die Anzahl der Joins und verbessert die Abfragegeschwindigkeit.\n\n"
                    "Wann ist Denormalisierung sinnvoll?\n\n"
                    "Leistungsanforderungen: Wenn die Abfrageleistung wichtiger ist als die Speichereffizienz, kann Denormalisierung sinnvoll sein. Dies gilt besonders in Data-Warehouse- oder Reporting-Systemen, "
                    "wo schnelle Lesezugriffe entscheidend sind.\n\n"
                    "Vermeidung komplexer Joins: In sehr großen Datenbanken können komplexe Joins die Abfrageleistung erheblich beeinträchtigen. Durch Denormalisierung werden die Daten in einer Weise strukturiert, "
                    "die diese Joins vermeidet.\n\n"
                    "Spezifische Anwendungsfälle: In bestimmten Anwendungsfällen, wie z.B. bei Echtzeit-Analysen oder in hochfrequentierten Webanwendungen, kann die Denormalisierung verwendet werden, "
                    "um die Datenbankleistung zu optimieren.\n\n"
                    "Zusammenfassung:\n\n"
                    "Normalisierung: Wichtig für die Vermeidung von Redundanz und zur Sicherstellung der Datenintegrität. Sie ist besonders nützlich in Systemen, in denen Datenkonsistenz und "
                    "Speicherplatzoptimierung von entscheidender Bedeutung sind.\n\n"
                    "Denormalisierung: Wird angewendet, wenn die Abfrageleistung von höherer Priorität ist als die Vermeidung von Redundanz. Dies ist besonders in Systemen sinnvoll, "
                    "in denen schnelle Datenzugriffe erforderlich sind."
                )
            }
        ],
        'sql_database_queries': [
            {
                'question': "1- Wie würden Sie eine SQL-Abfrage optimieren, die zu langsam ist?",
                 'answer': (
                    "Schritte zur Optimierung einer langsamen SQL-Abfrage:\n\n"
                    "1. Verwendung von Indizes:\n\n"
                    "Beschreibung: Indizes beschleunigen den Zugriff auf Daten, indem sie eine strukturierte Möglichkeit bieten, bestimmte Datensätze schnell zu finden.\n\n"
                    "Beispiel: Wenn eine Abfrage häufig eine WHERE-Bedingung auf einer bestimmten Spalte verwendet, könnte ein Index auf dieser Spalte die Abfragezeit erheblich verkürzen.\n\n"
                    "2. Vermeidung von SELECT *:\n\n"
                    "Beschreibung: SELECT * holt alle Spalten einer Tabelle, auch wenn nicht alle benötigt werden. Dies erhöht den I/O-Aufwand und verlangsamt die Abfrage.\n\n"
                    "Beispiel: Statt SELECT * sollte SELECT gefolgt von den benötigten Spalten verwendet werden, um nur die notwendigen Daten abzurufen.\n\n"
                    "3. Joins statt Subqueries:\n\n"
                    "Beschreibung: Subqueries können die Abfrageleistung beeinträchtigen, insbesondere wenn sie in WHERE-Klauseln verwendet werden. Joins sind in der Regel effizienter.\n\n"
                    "Beispiel: Statt einer Subquery innerhalb einer WHERE-Klausel kann ein JOIN verwendet werden, um die gleiche Funktionalität mit besserer Leistung zu erreichen.\n\n"
                    "4. Überprüfung und Optimierung des Abfrageausführungsplans:\n\n"
                    "Beschreibung: Moderne Datenbanksysteme bieten Tools, um den Abfrageausführungsplan zu analysieren. Dieser zeigt, wie die Datenbank die Abfrage ausführt und wo Engpässe auftreten könnten.\n\n"
                    "Beispiel: Ein DBA könnte den Ausführungsplan verwenden, um festzustellen, ob ein Full Table Scan stattfindet, und entscheiden, ob ein zusätzlicher Index erforderlich ist.\n\n"
                    "5. Partitionierung großer Tabellen:\n\n"
                    "Beschreibung: Große Tabellen können in kleinere, besser verwaltbare Teile (Partitionen) aufgeteilt werden, was die Abfrageleistung verbessert.\n\n"
                    "Beispiel: Eine Tabelle, die Bestellungen nach Jahren speichert, könnte in Jahrespartitionen aufgeteilt werden, sodass eine Abfrage nur die relevante Partition durchsucht.\n\n"
                    "6. Datenbankkonfiguration und Hardware-Optimierung:\n\n"
                    "Beschreibung: Datenbankeinstellungen wie Speicherzuweisungen, Cache-Größen und die Konfiguration der Festplatten-I/O können angepasst werden, um die Leistung zu verbessern.\n\n"
                    "Beispiel: Erhöhen der Cache-Größe für häufig genutzte Daten oder Optimierung des RAID-Setups für schnellere Schreib-/Leseoperationen.\n\n"
                    "7. Verwendung von Materialized Views:\n\n"
                    "Beschreibung: Materialized Views speichern die Ergebnisse einer komplexen Abfrage, sodass diese nicht bei jeder Ausführung neu berechnet werden müssen.\n\n"
                    "Beispiel: Wenn eine Abfrage komplexe Berechnungen oder Joins über mehrere Tabellen enthält, kann eine materialisierte Ansicht die Abfragegeschwindigkeit erhöhen.\n\n"
                    "Zusammenfassung:\n\n"
                    "Indizes hinzufügen: Wichtig für schnelle Datenzugriffe.\n\n"
                    "Vermeidung von SELECT *: Reduziert die Menge der abgerufenen Daten.\n\n"
                    "Joins statt Subqueries: Effizienter für die Kombination von Daten aus mehreren Tabellen.\n\n"
                    "Analyse des Abfrageausführungsplans: Identifizierung und Beseitigung von Engpässen.\n\n"
                    "Partitionierung und Materialized Views: Nützlich für große Datenmengen und komplexe Abfragen.\n\n"
                    "Optimierung der Hardware und Konfiguration: Kann die Gesamtleistung der Datenbank erhöhen."
                )
            },
            {
                'question': "2- Können Sie die verschiedenen JOIN-Typen in SQL erklären und wann Sie diese einsetzen würden (INNER, LEFT, RIGHT, FULL)?",
                'answer': (
                    "JOIN-Typen in SQL:\n\n"
                    "1. INNER JOIN:\n\n"
                    "Beschreibung: Der INNER JOIN gibt nur die Datensätze zurück, die in beiden Tabellen übereinstimmende Werte haben. Wenn keine Übereinstimmung gefunden wird, werden keine Zeilen in das Ergebnis aufgenommen.\n\n"
                    "Wann verwenden: Wenn Sie nur die Datensätze benötigen, die in beiden Tabellen vorhanden sind.\n\n"
                    "Beispiel:\n"
                    "```sql\n"
                    "SELECT Kunden.name, Bestellungen.bestellnummer\n"
                    "FROM Kunden\n"
                    "INNER JOIN Bestellungen ON Kunden.kunden_id = Bestellungen.kunden_id;\n"
                    "```\n\n"
                    "2. LEFT JOIN (LEFT OUTER JOIN):\n\n"
                    "Beschreibung: Der LEFT JOIN gibt alle Datensätze aus der linken Tabelle zurück und die übereinstimmenden Datensätze aus der rechten Tabelle. Wenn keine Übereinstimmung in der rechten Tabelle gefunden wird, wird NULL zurückgegeben.\n\n"
                    "Wann verwenden: Wenn Sie alle Datensätze aus der linken Tabelle benötigen, auch wenn keine Übereinstimmung in der rechten Tabelle vorhanden ist.\n\n"
                    "Beispiel:\n"
                    "```sql\n"
                    "SELECT Kunden.name, Bestellungen.bestellnummer\n"
                    "FROM Kunden\n"
                    "LEFT JOIN Bestellungen ON Kunden.kunden_id = Bestellungen.kunden_id;\n"
                    "```\n\n"
                    "3. RIGHT JOIN (RIGHT OUTER JOIN):\n\n"
                    "Beschreibung: Der RIGHT JOIN gibt alle Datensätze aus der rechten Tabelle zurück und die übereinstimmenden Datensätze aus der linken Tabelle. Wenn keine Übereinstimmung in der linken Tabelle gefunden wird, wird NULL zurückgegeben.\n\n"
                    "Wann verwenden: Wenn Sie alle Datensätze aus der rechten Tabelle benötigen, auch wenn keine Übereinstimmung in der linken Tabelle vorhanden ist.\n\n"
                    "Beispiel:\n"
                    "```sql\n"
                    "SELECT Kunden.name, Bestellungen.bestellnummer\n"
                    "FROM Kunden\n"
                    "RIGHT JOIN Bestellungen ON Kunden.kunden_id = Bestellungen.kunden_id;\n"
                    "```\n\n"
                    "4. FULL JOIN (FULL OUTER JOIN):\n\n"
                    "Beschreibung: Der FULL JOIN gibt alle Datensätze zurück, wenn es eine Übereinstimmung in entweder der linken oder der rechten Tabelle gibt. Wenn keine Übereinstimmung in einer Tabelle gefunden wird, wird NULL zurückgegeben.\n\n"
                    "Wann verwenden: Wenn Sie alle Datensätze aus beiden Tabellen benötigen, unabhängig davon, ob eine Übereinstimmung vorhanden ist oder nicht.\n\n"
                    "Beispiel:\n"
                    "```sql\n"
                    "SELECT Kunden.name, Bestellungen.bestellnummer\n"
                    "FROM Kunden\n"
                    "FULL OUTER JOIN Bestellungen ON Kunden.kunden_id = Bestellungen.kunden_id;\n"
                    "```\n\n"
                    "Zusammenfassung:\n\n"
                    "INNER JOIN: Nur übereinstimmende Datensätze aus beiden Tabellen.\n\n"
                    "LEFT JOIN: Alle Datensätze aus der linken Tabelle und übereinstimmende aus der rechten Tabelle.\n\n"
                    "RIGHT JOIN: Alle Datensätze aus der rechten Tabelle und übereinstimmende aus der linken Tabelle.\n\n"
                    "FULL JOIN: Alle Datensätze aus beiden Tabellen, unabhängig von Übereinstimmungen."
                )
            },
            {
                'question': "3- Wie würden Sie eine komplexe Abfrage schreiben, die Daten aus mehreren Tabellen kombiniert und filtert?",
                'answer': (
                    "Eine komplexe SQL-Abfrage, die Daten aus mehreren Tabellen kombiniert und filtert, erfordert die Verwendung von Joins, Aggregatfunktionen und Filterbedingungen. Hier ist ein Beispiel und eine ausführliche Erklärung:\n\n"
                    "Beispiel:\n\n"
                    "Angenommen, wir haben die folgenden Tabellen in einer E-Commerce-Datenbank:\n\n"
                    "- **Kunden** (`Kunden`): Speichert Informationen über Kunden.\n"
                    "  - `kunden_id`: Primärschlüssel\n"
                    "  - `name`: Name des Kunden\n"
                    "  - `email`: E-Mail-Adresse des Kunden\n\n"
                    "- **Bestellungen** (`Bestellungen`): Speichert Informationen über Bestellungen.\n"
                    "  - `bestellnummer`: Primärschlüssel\n"
                    "  - `kunden_id`: Fremdschlüssel zu `Kunden`\n"
                    "  - `bestelldatum`: Datum der Bestellung\n\n"
                    "- **Bestellpositionen** (`Bestellpositionen`): Speichert Informationen über die einzelnen Artikel in einer Bestellung.\n"
                    "  - `bestellposition_id`: Primärschlüssel\n"
                    "  - `bestellnummer`: Fremdschlüssel zu `Bestellungen`\n"
                    "  - `produkt_id`: Fremdschlüssel zu `Produkte`\n"
                    "  - `menge`: Anzahl der bestellten Artikel\n"
                    "  - `preis`: Preis pro Artikel\n\n"
                    "- **Produkte** (`Produkte`): Speichert Informationen über Produkte.\n"
                    "  - `produkt_id`: Primärschlüssel\n"
                    "  - `name`: Name des Produkts\n"
                    "  - `kategorie`: Kategorie des Produkts\n"
                    "  - `preis`: Preis des Produkts\n\n"
                    "Ziel der Abfrage:\n\n"
                    "Wir möchten eine Abfrage erstellen, die die folgenden Informationen zurückgibt:\n\n"
                    "- Den Namen des Kunden\n"
                    "- Das Bestelldatum\n"
                    "- Den Namen des Produkts\n"
                    "- Die Anzahl der bestellten Artikel\n"
                    "- Den Gesamtpreis der Bestellung\n"
                    "- Nur Bestellungen, bei denen der Gesamtpreis mehr als 100 Euro beträgt\n\n"
                    "SQL-Abfrage:\n\n"
                    "```sql\n"
                    "SELECT \n"
                    "    k.name AS kundenname, \n"
                    "    b.bestelldatum, \n"
                    "    p.name AS produktname, \n"
                    "    bp.menge, \n"
                    "    (bp.menge * bp.preis) AS gesamtpreis\n"
                    "FROM \n"
                    "    Kunden k\n"
                    "JOIN \n"
                    "    Bestellungen b ON k.kunden_id = b.kunden_id\n"
                    "JOIN \n"
                    "    Bestellpositionen bp ON b.bestellnummer = bp.bestellnummer\n"
                    "JOIN \n"
                    "    Produkte p ON bp.produkt_id = p.produkt_id\n"
                    "WHERE \n"
                    "    (bp.menge * bp.preis) > 100\n"
                    "ORDER BY \n"
                    "    b.bestelldatum DESC;\n"
                    "```\n\n"
                    "Erklärung der Abfrage:\n\n"
                    "1. **JOINs**: Die Abfrage verbindet die Tabellen `Kunden`, `Bestellungen`, `Bestellpositionen` und `Produkte` miteinander, um die notwendigen Daten aus allen Tabellen zu kombinieren.\n\n"
                    "2. **SELECT-Klausel**: Wir wählen spezifische Spalten aus, die wir anzeigen möchten und benennen diese, um sie im Ergebnis besser lesbar zu machen.\n\n"
                    "3. **WHERE-Klausel**: Diese Bedingung filtert die Ergebnisse, sodass nur Bestellungen zurückgegeben werden, bei denen der Gesamtpreis größer als 100 Euro ist.\n\n"
                    "4. **ORDER BY-Klausel**: Die Ergebnisse werden nach dem Bestelldatum in absteigender Reihenfolge sortiert.\n\n"
                    "5. **Aggregatfunktion**: `(bp.menge * bp.preis)` berechnet den Gesamtpreis für jede Bestellposition und wird in der WHERE-Klausel verwendet.\n\n"
                    "Diese Abfrage ist ein Beispiel dafür, wie man komplexe Datenabfragen strukturiert und filtert, um spezifische Informationen aus mehreren Tabellen in einer relationalen Datenbank zu extrahieren."
                )
            },
            {
                'question': "4- Wie gehen Sie mit Deadlocks in einer Datenbank um?",
                'answer': (
                    "Ein Deadlock tritt auf, wenn zwei oder mehr Transaktionen gegenseitig auf Ressourcen warten, die von einer anderen Transaktion gehalten werden, was dazu führt, dass keine der Transaktionen fortfahren kann. Dies kann in einer Datenbank auftreten, wenn mehrere Transaktionen auf die gleichen Daten zugreifen und diese in unterschiedlicher Reihenfolge sperren. Hier sind einige Strategien, um mit Deadlocks umzugehen:\n\n"
                    "**1. Ursachenanalyse und Identifizierung**:\n\n"
                    "- **Transaktionsanalyse**: Identifizieren Sie die Transaktionen, die an einem Deadlock beteiligt sind.\n"
                    "- **Query-Optimierung**: Überprüfen Sie die SQL-Abfragen, um sicherzustellen, dass sie so optimiert sind, dass sie nur die notwendigen Daten sperren.\n\n"
                    "**2. Verwendung von Transaktionsisolationsebenen**:\n\n"
                    "- **Isolationslevel senken**: Durch die Senkung des Isolationslevels können Sperren vermieden werden.\n"
                    "- **Optimistisches Sperren**: Verwenden Sie optimistisches Sperren, bei dem die Ressource erst bei der Commit-Phase gesperrt wird.\n\n"
                    "**3. Sperrstrategie verbessern**:\n\n"
                    "- **Konsistente Sperrreihenfolge**: Stellen Sie sicher, dass alle Transaktionen in derselben Reihenfolge auf Ressourcen zugreifen.\n"
                    "- **Vermeiden von langen Transaktionen**: Halten Sie Transaktionen so kurz wie möglich.\n\n"
                    "**4. Verwendung von Zeitüberschreitungen (Timeouts)**:\n\n"
                    "- **Transaktions-Timeouts**: Implementieren Sie Zeitüberschreitungen für Transaktionen.\n\n"
                    "**5. Deadlock-Erkennung und -Wiederherstellung**:\n\n"
                    "- **Automatische Deadlock-Erkennung**: Viele Datenbanksysteme bieten Mechanismen zur automatischen Deadlock-Erkennung.\n"
                    "- **Manuelle Wiederherstellung**: In einigen Fällen kann es notwendig sein, manuell einzugreifen.\n\n"
                    "**6. Wiederholung fehlgeschlagener Transaktionen**:\n\n"
                    "- **Transaktionswiederholung**: Wenn eine Transaktion aufgrund eines Deadlocks abgebrochen wurde, sollte die Anwendung so gestaltet sein, dass die Transaktion erneut versucht wird.\n\n"
                    "**Beispiel**:\n"
                    "Angenommen, in einer Datenbank greifen zwei Transaktionen A und B auf zwei Tabellen X und Y zu. Transaktion A sperrt Tabelle X und versucht dann, auf Tabelle Y zuzugreifen, während Transaktion B Tabelle Y sperrt und versucht, auf Tabelle X zuzugreifen. Um diesen Deadlock zu vermeiden, könnte man sicherstellen, dass alle Transaktionen immer zuerst auf Tabelle X und dann auf Tabelle Y zugreifen, um die konsistente Sperrreihenfolge zu wahren."
                )
            }
        ],
        'database_design_architecture': [
             {
                'question': "1- Wie würden Sie eine Datenbank für eine Anwendung entwerfen, die eine große Anzahl von Lese- und Schreiboperationen bewältigen muss?",
                'answer': (
                    "Das Design einer Datenbank, die eine hohe Anzahl von Lese- und Schreiboperationen effizient bewältigen kann, erfordert sorgfältige Planung und Optimierung in mehreren Bereichen. Hier sind die wichtigsten Ansätze und Überlegungen:\n\n"
                    "**1. Horizontale Skalierung (Sharding)**:\n\n"
                    "- **Sharding**: Horizontale Skalierung, auch Sharding genannt, teilt die Datenbank in kleinere, verwaltbare Teile (Shards) auf, die auf verschiedenen Servern gespeichert werden.\n"
                    "- **Sharding-Strategie**: Wählen Sie eine geeignete Sharding-Strategie, z.B. basierend auf dem Benutzer, geografische Regionen oder andere Kriterien, die eine gleichmäßige Verteilung der Last gewährleisten.\n\n"
                    "**2. Caching**:\n\n"
                    "- **Implementierung von Caching**: Verwenden Sie Caching-Techniken, um häufig abgefragte Daten im Speicher zu halten. Dies reduziert die Anzahl der direkten Datenbankzugriffe und verbessert die Leseleistung erheblich.\n"
                    "- **Beispiele für Caching-Systeme**: Redis und Memcached sind beliebte In-Memory-Caching-Systeme.\n\n"
                    "**3. Datenbankindizes**:\n\n"
                    "- **Indizierung**: Fügen Sie Indizes zu den Spalten hinzu, die häufig in Abfragen verwendet werden, insbesondere in WHERE-, JOIN- und ORDER BY-Klauseln.\n"
                    "- **Berücksichtigung der Schreiblast**: Stellen Sie sicher, dass die Schreiboperationen nicht zu stark beeinträchtigt werden.\n\n"
                    "**4. Replikation**:\n\n"
                    "- **Replikation**: Setzen Sie Datenbank-Replikation ein, um mehrere Kopien der Datenbank auf verschiedenen Servern zu erstellen.\n"
                    "- **Master-Slave- oder Master-Master-Replikation**: Verwenden Sie Master-Slave-Replikation für Szenarien mit hoher Leseaktivität.\n\n"
                    "**5. Partitionierung**:\n\n"
                    "- **Partitionierung von Tabellen**: Partitionieren Sie große Tabellen, um die Leistung zu verbessern.\n"
                    "- **Vorteile der Partitionierung**: Partitionierung kann die Abfrageleistung verbessern.\n\n"
                    "**6. Optimierung der Datenbankkonfiguration**:\n\n"
                    "- **Anpassung der Datenbankparameter**: Passen Sie Datenbankparameter wie Buffergrößen an.\n"
                    "- **Hardware-Ressourcen**: Stellen Sie sicher, dass die Datenbank auf leistungsstarker Hardware ausgeführt wird.\n\n"
                    "**7. Verwendung von NoSQL-Datenbanken (wenn angebracht)**:\n\n"
                    "- **NoSQL für spezifische Szenarien**: In Szenarien, in denen eine sehr hohe Skalierbarkeit erforderlich ist, kann der Einsatz einer NoSQL-Datenbank in Erwägung gezogen werden.\n"
                    "- **Polyglot-Persistence**: In einigen Fällen kann es sinnvoll sein, sowohl relationale als auch NoSQL-Datenbanken zu kombinieren.\n\n"
                    "**Beispiel**:\n"
                    "Eine E-Commerce-Website, die Millionen von Nutzern bedient und gleichzeitig zahlreiche Produktinformationen und Bestellungen verarbeiten muss, könnte eine Kombination aus horizontaler Skalierung, Caching und Replikation verwenden."
                )
            },
            {
                'question': "2- Können Sie ein Beispiel für ein Schema-Design für eine E-Commerce-Anwendung beschreiben?",
                'answer': (
                    "Ein Schema-Design für eine E-Commerce-Anwendung umfasst die Strukturierung der Daten in mehreren Tabellen, die verschiedene Entitäten des Geschäftsprozesses repräsentieren. Hier ist ein Beispiel für ein grundlegendes Schema-Design:\n\n"
                    "**1. Tabelle: Customers**:\n\n"
                    "- **Zweck**: Speicherung von Kundeninformationen.\n"
                    "- **Attribute**:\n"
                    "  - `id`: Primärschlüssel, eindeutige Identifikation des Kunden.\n"
                    "  - `first_name`: Vorname des Kunden.\n"
                    "  - `last_name`: Nachname des Kunden.\n"
                    "  - `email`: E-Mail-Adresse des Kunden, muss eindeutig sein.\n"
                    "  - `address`: Physische Adresse des Kunden.\n"
                    "  - `city`: Stadt, in der der Kunde wohnt.\n"
                    "  - `postal_code`: Postleitzahl des Kunden.\n"
                    "  - `country`: Land, in dem der Kunde wohnt.\n"
                    "  - `phone_number`: Telefonnummer des Kunden.\n\n"
                    "**2. Tabelle: Products**:\n\n"
                    "- **Zweck**: Speicherung von Produktinformationen.\n"
                    "- **Attribute**:\n"
                    "  - `id`: Primärschlüssel, eindeutige Identifikation des Produkts.\n"
                    "  - `name`: Name des Produkts.\n"
                    "  - `description`: Beschreibung des Produkts.\n"
                    "  - `price`: Preis des Produkts.\n"
                    "  - `category`: Kategorie, zu der das Produkt gehört (z.B. Elektronik, Kleidung).\n"
                    "  - `inventory`: Verfügbare Anzahl dieses Produkts im Lager.\n\n"
                    "**3. Tabelle: Orders**:\n\n"
                    "- **Zweck**: Speicherung von Bestellinformationen.\n"
                    "- **Attribute**:\n"
                    "  - `id`: Primärschlüssel, eindeutige Identifikation der Bestellung.\n"
                    "  - `customer_id`: Fremdschlüssel, der auf die `Customers`-Tabelle verweist.\n"
                    "  - `order_date`: Datum und Uhrzeit, zu der die Bestellung aufgegeben wurde.\n"
                    "  - `shipping_address`: Versandadresse, falls sie von der Kundenadresse abweicht.\n"
                    "  - `billing_address`: Rechnungsadresse, falls sie von der Kundenadresse abweicht.\n\n"
                    "**4. Tabelle: OrderItems**:\n\n"
                    "- **Zweck**: Speicherung der Produkte, die mit einer bestimmten Bestellung verknüpft sind.\n"
                    "- **Attribute**:\n"
                    "  - `id`: Primärschlüssel, eindeutige Identifikation des Bestellitems.\n"
                    "  - `order_id`: Fremdschlüssel, der auf die `Orders`-Tabelle verweist.\n"
                    "  - `product_id`: Fremdschlüssel, der auf die `Products`-Tabelle verweist.\n"
                    "  - `quantity`: Anzahl der bestellten Einheiten dieses Produkts.\n"
                    "  - `price`: Preis des Produkts zum Zeitpunkt der Bestellung.\n\n"
                    "**Beziehungen zwischen den Tabellen**:\n"
                    "- **Customers** und **Orders**: Eine 1:n-Beziehung.\n"
                    "- **Orders** und **OrderItems**: Eine 1:n-Beziehung.\n"
                    "- **Products** und **OrderItems**: Eine 1:n-Beziehung.\n\n"
                    "**Beispiel**:\n"
                    "Angenommen, ein Kunde bestellt zwei verschiedene Produkte. Die Bestellung würde in der `Orders`-Tabelle gespeichert, und die einzelnen Produkte dieser Bestellung würden in der `OrderItems`-Tabelle aufgeführt."
                )
            },
            {
                'question': "3- Wie würden Sie mit dem Problem der Datenbankmigration umgehen, wenn sich das Schema in einer produktiven Umgebung ändert?",
                'answer': (
                    "Der Umgang mit Datenbankmigrationen in einer produktiven Umgebung erfordert sorgfältige Planung und präzise Durchführung, um sicherzustellen, dass die Datenintegrität erhalten bleibt und der Betrieb der Anwendung nicht unterbrochen wird. Hier sind die wichtigsten Schritte:\n\n"
                    "**1. Versionskontrolle für das Datenbankschema**:\n"
                    "Verwenden Sie Tools wie Flyway, Liquibase oder die integrierten Migrations-Tools von Frameworks wie Django (Django Migrations) oder Rails (ActiveRecord Migrations), um das Schema zu versionieren.\n\n"
                    "**2. Testen in einer Staging-Umgebung**:\n"
                    "Führen Sie alle Migrationen zunächst in einer Staging- oder Testumgebung durch.\n\n"
                    "**3. Backup der Datenbank**:\n"
                    "Vor jeder Migration sollten vollständige Backups der Produktionsdatenbank erstellt werden.\n\n"
                    "**4. Downtime planen oder Zero-Downtime-Strategien implementieren**:\n"
                    "Wenn die Migration zu umfangreichen Änderungen führt, kann eine geplante Downtime erforderlich sein.\n\n"
                    "**5. Rollback-Strategien vorbereiten**:\n"
                    "Es ist wichtig, eine klare Rollback-Strategie zu haben, falls bei der Migration Probleme auftreten.\n\n"
                    "**6. Migrationsstrategien für große Datenmengen**:\n"
                    "Wenn das Schema Änderungen an großen Tabellen erfordert, sollten Techniken wie das schrittweise Migrieren von Daten in Betracht gezogen werden.\n\n"
                    "**7. Überwachung und Validierung nach der Migration**:\n"
                    "Nach der Migration sollte die Datenbank sorgfältig überwacht werden, um sicherzustellen, dass sie wie erwartet funktioniert.\n\n"
                    "**Beispiel**:\n"
                    "Angenommen, Sie müssen eine neue Spalte zu einer stark frequentierten Tabelle hinzufügen. Eine schrittweise Vorgehensweise minimiert das Risiko und gewährleistet eine unterbrechungsfreie Umstellung."
                )
            }
        ]
    }

    context = {
        'section_title': sections.get(section, 'Questions and Answers'),
        'questions_and_answers': questions_and_answers.get(section, [])
    }
    return render(request, 'store/questions_detail.html', context)
