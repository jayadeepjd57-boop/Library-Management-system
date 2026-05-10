"""
╔══════════════════════════════════════════════════════════╗
║  AMRITA LIBRARY MANAGEMENT SYSTEM — Python Backend       ║
║  Algorithms: Quicksort, Binary Search, Linear Search,    ║
║              Fine Calculator, Max-Heap Sort              ║
╚══════════════════════════════════════════════════════════╝
"""

import json, datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ── CONFIG ───────────────────────────────────────────────
FINE_RATE = 5   # ₹5 per overdue day

# ── DATA ─────────────────────────────────────────────────
BOOKS = [
    {"id":101,"name":"Data Structures",        "author":"Mark Allen",           "status":"Available"},
    {"id":102,"name":"Java Programming",        "author":"James Gosling",        "status":"Issued"},
    {"id":103,"name":"Operating Systems",       "author":"Abraham Silberschatz", "status":"Available"},
    {"id":104,"name":"Computer Networks",       "author":"Andrew Tanenbaum",     "status":"Available"},
    {"id":105,"name":"Database Systems",        "author":"Raghu Ramakrishnan",   "status":"Issued"},
    {"id":106,"name":"Python Programming",      "author":"Guido van Rossum",     "status":"Available"},
    {"id":107,"name":"Machine Learning",        "author":"Tom Mitchell",         "status":"Available"},
    {"id":108,"name":"Artificial Intelligence", "author":"Stuart Russell",       "status":"Issued"},
    {"id":109,"name":"Software Engineering",    "author":"Ian Sommerville",      "status":"Available"},
    {"id":110,"name":"Computer Graphics",             "author":"Donald Hearn",             "status":"Available"},
    {"id":111,"name":"Discrete Mathematics",          "author":"Kenneth Rosen",            "status":"Available"},
    {"id":112,"name":"Algorithm Design",              "author":"Jon Kleinberg",            "status":"Available"},
    {"id":113,"name":"Introduction to Algorithms",    "author":"Thomas H. Cormen",         "status":"Issued"},
    {"id":114,"name":"Computer Architecture",         "author":"John L. Hennessy",         "status":"Available"},
    {"id":115,"name":"Digital Logic Design",          "author":"Morris Mano",              "status":"Available"},
    {"id":116,"name":"Theory of Computation",         "author":"Michael Sipser",           "status":"Available"},
    {"id":117,"name":"Compiler Design",               "author":"Alfred Aho",               "status":"Issued"},
    {"id":118,"name":"Embedded Systems",              "author":"Jonathan Valvano",         "status":"Available"},
    {"id":119,"name":"Cloud Computing",               "author":"Rajkumar Buyya",           "status":"Available"},
    {"id":120,"name":"Cyber Security Essentials",     "author":"Charles Brooks",           "status":"Available"},
    {"id":121,"name":"Cryptography and Network Security","author":"William Stallings",     "status":"Issued"},
    {"id":122,"name":"Deep Learning",                 "author":"Ian Goodfellow",           "status":"Available"},
    {"id":123,"name":"Neural Networks",               "author":"Simon Haykin",             "status":"Available"},
    {"id":124,"name":"Natural Language Processing",   "author":"Daniel Jurafsky",          "status":"Available"},
    {"id":125,"name":"Computer Vision",               "author":"Richard Szeliski",         "status":"Available"},
    {"id":126,"name":"Robotics: Modelling and Control","author":"Mark Spong",             "status":"Issued"},
    {"id":127,"name":"Internet of Things",            "author":"Arshdeep Bahga",           "status":"Available"},
    {"id":128,"name":"Big Data Analytics",            "author":"V.K. Jain",               "status":"Available"},
    {"id":129,"name":"Data Mining Concepts",          "author":"Jiawei Han",               "status":"Available"},
    {"id":130,"name":"Information Retrieval",         "author":"Christopher Manning",      "status":"Available"},
    {"id":131,"name":"Probability and Statistics",    "author":"Sheldon Ross",             "status":"Issued"},
    {"id":132,"name":"Linear Algebra",                "author":"Gilbert Strang",           "status":"Available"},
    {"id":133,"name":"Calculus",                      "author":"James Stewart",            "status":"Available"},
    {"id":134,"name":"Numerical Methods",             "author":"S.S. Sastry",              "status":"Available"},
    {"id":135,"name":"Graph Theory",                  "author":"Frank Harary",             "status":"Available"},
    {"id":136,"name":"Automata Theory",               "author":"John E. Hopcroft",         "status":"Issued"},
    {"id":137,"name":"Parallel Computing",            "author":"Barry Wilkinson",          "status":"Available"},
    {"id":138,"name":"Distributed Systems",           "author":"Andrew Tanenbaum",         "status":"Available"},
    {"id":139,"name":"Mobile Computing",              "author":"Raj Kamal",                "status":"Available"},
    {"id":140,"name":"Wireless Networks",             "author":"William Stallings",        "status":"Available"},
    {"id":141,"name":"Linux Command Line",            "author":"William Shotts",           "status":"Issued"},
    {"id":142,"name":"Unix Programming",              "author":"W. Richard Stevens",       "status":"Available"},
    {"id":143,"name":"TCP/IP Illustrated",            "author":"W. Richard Stevens",       "status":"Available"},
    {"id":144,"name":"Web Technologies",              "author":"Chris Bates",              "status":"Available"},
    {"id":145,"name":"JavaScript: The Good Parts",    "author":"Douglas Crockford",        "status":"Available"},
    {"id":146,"name":"Clean Code",                    "author":"Robert C. Martin",         "status":"Issued"},
    {"id":147,"name":"Design Patterns",               "author":"Gang of Four",             "status":"Available"},
    {"id":148,"name":"Refactoring",                   "author":"Martin Fowler",            "status":"Available"},
    {"id":149,"name":"Agile Software Development",    "author":"Robert C. Martin",         "status":"Available"},
    {"id":150,"name":"The Pragmatic Programmer",      "author":"David Thomas",             "status":"Available"},
    {"id":151,"name":"Code Complete",                 "author":"Steve McConnell",          "status":"Issued"},
    {"id":152,"name":"Head First Design Patterns",    "author":"Eric Freeman",             "status":"Available"},
    {"id":153,"name":"Object Oriented Analysis",      "author":"Grady Booch",              "status":"Available"},
    {"id":154,"name":"UML Distilled",                 "author":"Martin Fowler",            "status":"Available"},
    {"id":155,"name":"System Design Interview",       "author":"Alex Xu",                  "status":"Available"},
    {"id":156,"name":"Database Management Systems",   "author":"C.J. Date",               "status":"Issued"},
    {"id":157,"name":"SQL for Data Analysis",         "author":"Cathy Tanimura",           "status":"Available"},
    {"id":158,"name":"NoSQL Distilled",               "author":"Martin Fowler",            "status":"Available"},
    {"id":159,"name":"MongoDB: The Definitive Guide", "author":"Kristina Chodorow",        "status":"Available"},
    {"id":160,"name":"Redis in Action",               "author":"Josiah Carlson",           "status":"Available"},
    {"id":161,"name":"Elasticsearch in Action",       "author":"Radu Gheorghe",            "status":"Issued"},
    {"id":162,"name":"Kafka: The Definitive Guide",   "author":"Neha Narkhede",            "status":"Available"},
    {"id":163,"name":"Hadoop: The Definitive Guide",  "author":"Tom White",                "status":"Available"},
    {"id":164,"name":"Spark: The Definitive Guide",   "author":"Bill Chambers",            "status":"Available"},
    {"id":165,"name":"Docker Deep Dive",              "author":"Nigel Poulton",            "status":"Available"},
    {"id":166,"name":"Kubernetes in Action",          "author":"Marko Luksa",              "status":"Issued"},
    {"id":167,"name":"DevOps Handbook",               "author":"Gene Kim",                 "status":"Available"},
    {"id":168,"name":"Site Reliability Engineering",  "author":"Betsy Beyer",              "status":"Available"},
    {"id":169,"name":"Microservices Patterns",        "author":"Chris Richardson",         "status":"Available"},
    {"id":170,"name":"Building Microservices",        "author":"Sam Newman",               "status":"Available"},
    {"id":171,"name":"RESTful Web APIs",              "author":"Leonard Richardson",       "status":"Issued"},
    {"id":172,"name":"GraphQL in Action",             "author":"Samer Buna",               "status":"Available"},
    {"id":173,"name":"Computer Science Distilled",    "author":"Wladston Ferreira",        "status":"Available"},
    {"id":174,"name":"Structure and Interpretation",  "author":"Harold Abelson",           "status":"Available"},
    {"id":175,"name":"The Art of Computer Programming","author":"Donald Knuth",            "status":"Available"},
    {"id":176,"name":"Programming Pearls",            "author":"Jon Bentley",              "status":"Issued"},
    {"id":177,"name":"C Programming Language",        "author":"Dennis Ritchie",           "status":"Available"},
    {"id":178,"name":"C++ Primer",                    "author":"Stanley Lippman",          "status":"Available"},
    {"id":179,"name":"Effective C++",                 "author":"Scott Meyers",             "status":"Available"},
    {"id":180,"name":"The Rust Programming Language", "author":"Steve Klabnik",            "status":"Available"},
    {"id":181,"name":"Go Programming Language",       "author":"Alan Donovan",             "status":"Issued"},
    {"id":182,"name":"Kotlin in Action",              "author":"Dmitry Jemerov",           "status":"Available"},
    {"id":183,"name":"Swift Programming",             "author":"Apple Inc.",               "status":"Available"},
    {"id":184,"name":"Learning Python",               "author":"Mark Lutz",                "status":"Available"},
    {"id":185,"name":"Fluent Python",                 "author":"Luciano Ramalho",          "status":"Available"},
    {"id":186,"name":"Automate the Boring Stuff",     "author":"Al Sweigart",              "status":"Issued"},
    {"id":187,"name":"Python Data Science Handbook",  "author":"Jake VanderPlas",          "status":"Available"},
    {"id":188,"name":"Hands-On Machine Learning",     "author":"Aurélien Géron",           "status":"Available"},
    {"id":189,"name":"Pattern Recognition",           "author":"Christopher Bishop",       "status":"Available"},
    {"id":190,"name":"Reinforcement Learning",        "author":"Richard Sutton",           "status":"Available"},
    {"id":191,"name":"Generative AI Concepts",        "author":"David Foster",             "status":"Issued"},
    {"id":192,"name":"Ethics of Artificial Intelligence","author":"Nick Bostrom",          "status":"Available"},
    {"id":193,"name":"Human Computer Interaction",    "author":"Alan Dix",                 "status":"Available"},
    {"id":194,"name":"Game Programming Patterns",     "author":"Robert Nystrom",           "status":"Available"},
    {"id":195,"name":"3D Math Primer for Graphics",   "author":"Fletcher Dunn",            "status":"Available"},
    {"id":196,"name":"Quantum Computing",             "author":"Michael Nielsen",          "status":"Issued"},
    {"id":197,"name":"Blockchain Basics",             "author":"Daniel Drescher",          "status":"Available"},
    {"id":198,"name":"Digital Transformation",        "author":"Thomas Siebel",            "status":"Available"},
    {"id":199,"name":"The Phoenix Project",           "author":"Gene Kim",                 "status":"Available"},
    {"id":200,"name":"Mythical Man Month",            "author":"Frederick Brooks",         "status":"Available"},
    {"id":201,"name":"Zero to One",                   "author":"Peter Thiel",              "status":"Issued"},
    {"id":202,"name":"The Lean Startup",              "author":"Eric Ries",                "status":"Available"},
    {"id":203,"name":"Software Testing Fundamentals", "author":"Marnie Hutcheson",         "status":"Available"},
    {"id":204,"name":"Penetration Testing",           "author":"Georgia Weidman",          "status":"Available"},
    {"id":205,"name":"Network Security Essentials",   "author":"William Stallings",        "status":"Available"},
    {"id":206,"name":"Digital Forensics",             "author":"Eoghan Casey",             "status":"Issued"},
    {"id":207,"name":"Signals and Systems",           "author":"Alan Oppenheim",           "status":"Available"},
    {"id":208,"name":"Digital Signal Processing",     "author":"John Proakis",             "status":"Available"},
    {"id":209,"name":"VLSI Design",                   "author":"Wayne Wolf",               "status":"Available"},
    {"id":210,"name":"Microprocessors and Microcontrollers","author":"N.K. Maini",         "status":"Available"},
]

ISSUED_BOOKS = [
    {"student_id":"STUDENT1023","student_name":"TEAM 14",
     "book_id":101,"book_name":"Data Structures",
     "issue_date":"2026-03-01","due_date":"2026-03-10","returned":False},
    {"student_id":"STUDENT1023","student_name":"TEAM 14",
     "book_id":103,"book_name":"Operating Systems",
     "issue_date":"2026-02-25","due_date":"2026-03-09","returned":False},
]

# ════════════════════════════════════════════════════════
#  ALGORITHM 1 + 2 — QUICKSORT + BINARY SEARCH
# ════════════════════════════════════════════════════════
class BookSearch:

    # Algorithm 1: Quicksort O(n log n)
    @staticmethod
    def _qs(arr, lo, hi):
        if lo < hi:
            p = BookSearch._part(arr, lo, hi)
            BookSearch._qs(arr, lo, p-1)
            BookSearch._qs(arr, p+1, hi)

    @staticmethod
    def _part(arr, lo, hi):
        pivot, i = arr[hi]["id"], lo-1
        for j in range(lo, hi):
            if arr[j]["id"] <= pivot:
                i += 1; arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[hi] = arr[hi], arr[i+1]
        return i+1

    @staticmethod
    def sort(books):
        a = books[:]
        BookSearch._qs(a, 0, len(a)-1)
        return a

    # Algorithm 2: Binary Search O(log n)
    @staticmethod
    def by_id(books, target_id):
        s = BookSearch.sort(books)
        lo, hi = 0, len(s)-1
        while lo <= hi:
            mid = (lo+hi)//2
            if   s[mid]["id"] == target_id: return s[mid]
            elif s[mid]["id"] <  target_id: lo = mid+1
            else:                           hi = mid-1
        return None

    # Algorithm 3: Linear Search O(n)
    @staticmethod
    def by_keyword(books, kw):
        kw = kw.lower()
        return [b for b in books if kw in b["name"].lower() or kw in b["author"].lower()]


# ════════════════════════════════════════════════════════
#  ALGORITHM 4 + 5 — FINE CALCULATOR + MAX-HEAP SORT
# ════════════════════════════════════════════════════════
class FineCalc:

    # Algorithm 4: Fine per book O(1)
    @staticmethod
    def for_book(due_str, ret_str=None):
        due = datetime.date.fromisoformat(due_str)
        ret = datetime.date.fromisoformat(ret_str) if ret_str else datetime.date.today()
        return max(0, (ret - due).days * FINE_RATE)

    # Algorithm 5: All fines sorted descending (max-heap order) O(n log n)
    @staticmethod
    def all_sorted(issued):
        today = datetime.date.today()
        out = []
        for r in issued:
            if r.get("returned"): continue
            due  = datetime.date.fromisoformat(r["due_date"])
            days = max(0, (today - due).days)
            fine = days * FINE_RATE
            if fine > 0:
                out.append({
                    "student_id":   r["student_id"],
                    "student_name": r["student_name"],
                    "book_name":    r["book_name"],
                    "due_date":     r["due_date"],
                    "fine_amount":  fine,
                    "overdue_days": days,
                })
        out.sort(key=lambda x: x["fine_amount"], reverse=True)
        return out

    # Fine for a specific student
    @staticmethod
    def for_student(issued, student_id):
        today = datetime.date.today()
        result = []
        for r in issued:
            if r["student_id"] != student_id: continue
            due  = datetime.date.fromisoformat(r["due_date"])
            days = max(0, (today - due).days)
            fine = days * FINE_RATE
            result.append({
                "book_name":    r["book_name"],
                "issue_date":   r["issue_date"],
                "due_date":     r["due_date"],
                "returned":     r["returned"],
                "overdue_days": days if not r["returned"] else 0,
                "fine":         fine if not r["returned"] else 0,
            })
        return result


# ════════════════════════════════════════════════════════
#  HTTP API
# ════════════════════════════════════════════════════════
class API(BaseHTTPRequestHandler):

    def log_message(self, *a): pass

    def _ok(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type",                "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.send_header("Content-Length",              str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        p  = urlparse(self.path)
        qs = parse_qs(p.query)
        ep = p.path

        if ep == "/books":
            self._ok({"books": BOOKS})

        elif ep == "/search":
            if "id" in qs:
                try:
                    b = BookSearch.by_id(BOOKS, int(qs["id"][0]))
                    self._ok({"found": bool(b), "book": b})
                except ValueError:
                    self._ok({"error": "id must be integer"}, 400)
            elif "q" in qs:
                r = BookSearch.by_keyword(BOOKS, qs["q"][0])
                self._ok({"found": bool(r), "count": len(r), "books": r})
            else:
                self._ok({"error": "provide ?id= or ?q="}, 400)

        elif ep == "/fines":
            self._ok({"fines": FineCalc.all_sorted(ISSUED_BOOKS)})

        elif ep == "/profile":
            sid       = qs.get("student_id", ["STUDENT1023"])[0]
            fine_rows = FineCalc.for_student(ISSUED_BOOKS, sid)
            total     = sum(r["fine"] for r in fine_rows)
            self._ok({"student_id": sid, "books": fine_rows, "total_fine": total,
                      "as_of": str(datetime.date.today())})

        else:
            self._ok({"error": "not found"}, 404)

    def do_POST(self):
        n    = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n)) if n else {}
        ep   = urlparse(self.path).path

        if ep == "/add_book":
            req = {"id","name","author","status"}
            if missing := req - body.keys():
                self._ok({"error": f"missing: {list(missing)}"}); return
            if any(b["id"] == body["id"] for b in BOOKS):
                self._ok({"error": "ID exists"}, 409); return
            BOOKS.append(body)
            self._ok({"success": True, "book": body})

        elif ep == "/pay_fine":
            sid, bname = body.get("student_id"), body.get("book_name")
            for r in ISSUED_BOOKS:
                if r["student_id"] == sid and r["book_name"] == bname:
                    r["returned"] = True
                    self._ok({"success": True})
                    return
            self._ok({"error": "record not found"}, 404)

        else:
            self._ok({"error": "not found"}, 404)


# ════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════
if __name__ == "__main__":
    PORT = 8000
    print("=" * 50)
    print("  Amrita Library Backend → http://localhost:8000")
    print("=" * 50)
    HTTPServer(("localhost", PORT), API).serve_forever()
