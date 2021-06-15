from datetime import datetime
from sim import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(admin_id):
    return Tadmin.query.get(int(admin_id))

class Tprofil(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    sambutan = db.Column(db.Text, nullable=False)
    visi = db.Column(db.Text, nullable=False)
    misi = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"Tprofil('{self.sambutan}','{self.visi}','{self.misi}')"

class Tdataumum(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.String(10), nullable=False)
    jsekolah = db.Column(db.String(10), nullable=False)
    jsswasta = db.Column(db.String(10), nullable=False)
    jssnegeri = db.Column(db.String(10), nullable=False)
    jguru = db.Column(db.String(10), nullable=False)
    jgpns = db.Column(db.String(10), nullable=False)
    jghonor = db.Column(db.String(10), nullable=False)
    jkepsek = db.Column(db.String(10), nullable=False)
    jkeppns = db.Column(db.String(10), nullable=False)
    jkephonor = db.Column(db.String(10), nullable=False)
    jrombel = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Tdataumum('{self.tahun}','{self.jsekolah}','{self.jsswasta}','{self.jssnegeri}','{self.jguru}','{self.jgpns}','{self.jghonor}','{self.jkepsek}','{self.jkeppns}','{self.jskephonor}','{self.jrombel}')"

class Tdataumumfilter(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return f"Tdataumumfilter('{self.tahun}')"


class Tdatasekolah(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    npsn = db.Column(db.String(15), unique=True, nullable=False)
    sekolah = db.Column(db.String(30), nullable=False)
    alamat = db.Column(db.String(50), nullable=False)
    jenissklh = db.Column(db.String(30), nullable=False)
    namakepsek = db.Column(db.String(30), nullable=False)
    foto = db.Column(db.String(30))
    akresklh_id = db.Column (db.Integer, db.ForeignKey('takresklh.id'))
    kecamatan_id = db.Column (db.Integer, db.ForeignKey('tkecamatan.id'))
    
    def __repr__(self):
        return f"Tdatasekolah('{self.npsn}','{self.sekolah}','{self.alamat}','{self.jenissklh}','{self.namakepsek}','{self.foto}')"

class Takresklh(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    jenis_akreditas = db.Column(db.String(15), unique=True, nullable=False)
    informasi_akreditas = db.Column(db.String(100), nullable=True)
    usekolah = db.relationship('Tdatasekolah', backref='akeditassekolah',lazy=True)
    
    def __repr__(self):
        return f"Takresklh('{self.jenis_akreditas}','{self.informasi_akreditas}')"

class Tkecamatan(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    jenis_wilayah = db.Column(db.String(50), unique=True, nullable=False)
    informasi_wilayah = db.Column(db.String(100), nullable=True)
    psekolah = db.relationship('Tdatasekolah', backref='alamatsekolah',lazy=True)
    
    def __repr__(self):
        return f"Tkecamatan('{self.jenis_wilayah}','{self.informasi_wilayah}')"

class Tpengaduan (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    detail_pengaduan = db.Column(db.String(300), nullable=False)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Tpengaduan('{self.email}','{self.kategori}','{self.detail_pengaduan}','{self.tgl_post}')"

class Tadmin (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    foto = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Tadmin('{self.nama}','{self.email}','{self.password}','{self.foto}')"
    
class Tberita (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    judul = db.Column(db.String(100), nullable=False)
    berita = db.Column(db.String(120), nullable=False)
    foto = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Tberita('{self.tgl_post}','{self.judul}','{self.berita}','{self.foto}')"


class Tdata_kegiatan (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.String(50), nullable=False)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    judul = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(120), nullable=False)
    bidang = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    def __repr__(self):
        return f"Tdatakegiatan('{self.tahun}','{self.tgl_post}','{self.judul}','{self.program}','{self.bidang}','{self.status}')"

class Tinformasi (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    judul = db.Column(db.String(100), nullable=False)
    informasi = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Tinformasi('{self.tgl_post}','{self.judul}','{self.informasi}')"


