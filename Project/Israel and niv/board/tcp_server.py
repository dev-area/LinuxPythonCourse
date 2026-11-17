import socket

HOST = "0.0.0.0"
# 0.0.0.0 = להקשיב על כל כרטיסי הרשת של הלוח

PORT = 5000
# הפורט של ערוץ Control, לפי המסמך של לירן

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# יוצרים socket: AF_INET = רשת עם IP, SOCK_STREAM = TCP

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# מאפשר להריץ שוב מיד אחרי עצירה, בלי השגיאה "Address already in use"

server.bind((HOST, PORT))
# "תופס" את פורט 5000

server.listen()
# מתחיל להקשיב לחיבורים. לקוחות שמגיעים בזמן שהשרת עסוק מחכים בתור

print(f"TCP server listening on port {PORT}")

while True:
    # לולאה אינסופית: השרת מטפל בלקוח אחרי לקוח

    conn, addr = server.accept()
    # מחכה עד שלקוח מתחבר. conn = הערוץ ללקוח הזה, addr = הכתובת שלו
    print("Connected:", addr)

    data = conn.recv(1024)
    # מקבל עד 1024 בייטים מהלקוח
    print("Received:", data)

    conn.sendall(data)
    # מחזיר ללקוח בדיוק את מה שהוא שלח (echo)

    conn.close()
    # סוגר את החיבור עם הלקוח הזה, וחוזר לחכות ללקוח הבא