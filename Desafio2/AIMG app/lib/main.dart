import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeFirebase();
  runApp(const MyApp());
}

Future<void> initializeFirebase() async {
  FirebaseOptions firebaseOptions = FirebaseOptions(
      apiKey: "AIzaSyARE1K6vM4j_QZlDVFBhgC9vl7uaF0c7ho",
      authDomain: "plc-connect-ed3dd.firebaseapp.com",
      databaseURL: "https://plc-connect-ed3dd-default-rtdb.firebaseio.com",
      projectId: "plc-connect-ed3dd",
      storageBucket: "plc-connect-ed3dd.appspot.com",
      messagingSenderId: "689102691305",
      appId: "1:689102691305:web:7fdf7aa6e2bb2f700cc978",
      measurementId: "G-WESV9N1VQZ");

  await Firebase.initializeApp(options: firebaseOptions);
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Aimg App',
      theme: ThemeData(
        scaffoldBackgroundColor: Colors.lightGreen[200],
        appBarTheme: AppBarTheme(
          backgroundColor: Colors.green[800],
        ),
        colorScheme: ColorScheme.fromSwatch(
          primarySwatch: Colors.green,
        ),
        textTheme: TextTheme(
          headline6: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Aimg App'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool _isTrue = true;
  String _segundos = '00:00:00';
  String _valorLerdoplc = '';

  final DatabaseReference _ligadoRef =
      FirebaseDatabase.instance.reference().child('ligado');
  final DatabaseReference _segundosRef =
      FirebaseDatabase.instance.reference().child('segundotempo');
  final DatabaseReference _lerdoplcRef =
      FirebaseDatabase.instance.reference().child('lerdoplc');

  void _toggleBoolean() {
    setState(() {
      _isTrue = !_isTrue;
    });
    _ligadoRef.set(_isTrue); // Enviar o valor para o Firebase Realtime Database
  }

  String _formatDuration(Duration duration) {
    String twoDigits(int n) => n.toString().padLeft(2, '0');
   // String twoDigitMinutes = twoDigits(duration.inMinutes.remainder(60));
    String twoDigitSeconds = twoDigits(duration.inSeconds.remainder(60)* 2);
   // String twoDigitHours = twoDigits(duration.inHours);
    return "$twoDigitSeconds";
  }

  @override
  void initState() {
    super.initState();
    _segundosRef.onValue.listen((event) {
      final dynamic segundos = event.snapshot.value;
      if (segundos != null) {
        setState(() {
          _segundos = _formatDuration(Duration(seconds: segundos as int));
        });
      }
    });

    _lerdoplcRef.onValue.listen((event) {
      final dynamic valorLerdoplc = event.snapshot.value;
      if (valorLerdoplc != null) {
        setState(() {
          _valorLerdoplc = valorLerdoplc.toString();
        });
      }
    });
  }

  void _connectFirebase() async {
    try {
      await initializeFirebase();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Conectado ao Firebase!')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erro ao conectar ao Firebase: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          widget.title,
          style: Theme.of(context).textTheme.headline6,
        ),
        centerTitle: true,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Container(
              padding: EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.lightGreen[300],
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: Colors.white),
              ),
              child: Text(
                'Aperte para alterar o estado da luz',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ),
            SizedBox(height: 20),
            SizedBox(
              width: 300,
              height: 100,
              child: ElevatedButton(
                onPressed: _toggleBoolean,
                style: ElevatedButton.styleFrom(
                  primary: _isTrue ? Colors.white : Colors.black,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
                child: Text(
                  _isTrue ? 'Luz: Ligada' : 'Luz: Desligada',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: _isTrue ? Colors.black : Colors.white,
                  ),
                ),
              ),
            ),
            SizedBox(height: 20),
            Text(
              '$_segundos segundo${_segundos != '01:00:00' ? 's' : ''}',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 20),
            Text(
              'Valor lido do PLC: $_valorLerdoplc',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _connectFirebase,
              child: Text('Conectar com o Firebase'),
            ),
          ],
        ),
      ),
    );
  }
}
