



class Distribuidor {

  String? id;
  String? nombre;
  String? gerente;
  String? logo;
  String? direccion;

  //PREGUNTAR
  String? paginaWeb;

  String? telefono;
  String? email;

  DateTime? created;
  DateTime? lastUpdate;

  List? sucursales;

  Map<String, dynamic>? cordinates;
  Map<String, dynamic>? horarioAtencion;

  Distribuidor({
    this.id,
    this.gerente,
    this.logo,
    this.cordinates,
    this.direccion,
    this.sucursales,
    this.nombre,
    this.created,
    this.lastUpdate,
    this.paginaWeb,
    this.telefono,
    this.email,
    this.horarioAtencion,
  });

  // Factory constructor para crear una instancia desde un mapa JSON
  factory Distribuidor.fromJson(json, id) {
    return Distribuidor(
      id: id,
      nombre: json['nombre'],
      created: DateTime.parse(json['created']),
      lastUpdate: DateTime.parse(json['lastUpdate']),
      gerente: json['gerente'],
      cordinates: json['cordinates'] == null
          ? {}
          : json['cordinates'].cast<String, dynamic>(),
      logo: json['logo'],
      direccion: json['direccion'],
      sucursales: json['sucursales'],
      paginaWeb: json['paginaWeb'],
      telefono: json['telefono'],
      email: json['email'],
      horarioAtencion: json['horarioAtencion'].cast<String, dynamic>(),
    );
  }

  // Función para convertir la instancia actual en un mapa JSON
  Map<String, dynamic> toJson() {
    return {
      'gerente': gerente,
      'nombre': nombre,
      'id': id,
      'cordinates': cordinates,
      'logo': logo,
      'lastUpdate': lastUpdate!.toIso8601String(),
      'created': created!.toIso8601String(),
      'direccion': direccion,
      'paginaWeb': paginaWeb,
      'telefono': telefono,
      'email': email,
      'horarioAtencion': horarioAtencion,
      'sucursales': sucursales
    };
  }
}
