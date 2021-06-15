from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from sim.models import Tprofil, Tdataumum, Tdatasekolah, Takresklh, Tkecamatan, Tpengaduan, Tadmin, Tberita,Tinformasi,Tdata_kegiatan
from flask_ckeditor import CKEditorField


class profil(FlaskForm):
    sambutan = CKEditorField('Sambutan', validators=[DataRequired()])
    visi= CKEditorField('Visi', validators=[DataRequired()])
    misi= CKEditorField('Misi', validators=[DataRequired()])
    submit=SubmitField('Tambah')

class profil_edit(FlaskForm):
    sambutan = CKEditorField('Sambutan', validators=[DataRequired()])
    visi= CKEditorField('Visi', validators=[DataRequired()])
    misi= CKEditorField('Misi', validators=[DataRequired()])
    submit=SubmitField('Tambah')

class berita_F(FlaskForm):
    judul=StringField('Judul Berita', validators=[DataRequired()])
    berita= TextAreaField('Berita')
    foto=FileField('Banner Berita', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Tambah')
    
class berita_edit(FlaskForm):
    judul=StringField('Judul Berita', validators=[DataRequired()])
    berita= TextAreaField('Berita')
    foto=FileField('Banner Berita', validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Simpan')


class data_umum(FlaskForm):
    tahun=StringField('Tahun', validators=[DataRequired()])
    jlh_sekolah=StringField('Jumlah Sekolah', validators=[DataRequired()])
    jlh_sswasta=StringField('Jumlah Sekolah Swasta', validators=[DataRequired()])
    jlh_snegeri=StringField('Jumlah Sekolah Negeri', validators=[DataRequired()])
    jlh_guru=StringField('Jumlah Guru', validators=[DataRequired()])
    jlh_gpns=StringField('Jumlah Guru PNS', validators=[DataRequired()])
    jlh_ghonor=StringField('Jumlah Guru Non PNS', validators=[DataRequired()])
    jlh_kepsek=StringField('Jumlah Kepala Sekolah', validators=[DataRequired()])
    jlh_kpns=StringField('Jumlah Kepala Sekolah PNS', validators=[DataRequired()])
    jlh_khonor=StringField('Jumlah Kepala Sekolah Non PNS', validators=[DataRequired()])
    jlh_rombel=StringField('Jumlah Rombongan Belajar', validators=[DataRequired()])
    submit=SubmitField('Tambah')

class data_umumedit(FlaskForm):
    tahun=StringField('Tahun', validators=[DataRequired()])
    jlh_sekolah=StringField('Jumlah Sekolah', validators=[DataRequired()])
    jlh_sswasta=StringField('Jumlah Sekolah Swasta', validators=[DataRequired()])
    jlh_snegeri=StringField('Jumlah Sekolah Negeri', validators=[DataRequired()])
    jlh_guru=StringField('Jumlah Guru', validators=[DataRequired()])
    jlh_gpns=StringField('Jumlah Guru PNS', validators=[DataRequired()])
    jlh_ghonor=StringField('Jumlah Guru Non PNS', validators=[DataRequired()])
    jlh_kepsek=StringField('Jumlah Kepala Sekolah', validators=[DataRequired()])
    jlh_kpns=StringField('Jumlah Kepala Sekolah PNS', validators=[DataRequired()])
    jlh_khonor=StringField('Jumlah Kepala Sekolah Non PNS', validators=[DataRequired()])
    jlh_rombel=StringField('Jumlah Rombongan Belajar', validators=[DataRequired()])
    submit=SubmitField('Simpan')

class data_sekolah(FlaskForm):
    npsn=StringField('NPSN', validators=[DataRequired()])
    nama_sekolah=StringField('Nama Kesatuan', validators=[DataRequired()])
    alamat=StringField('Desa/Kelurahan', validators=[DataRequired()])
    kecamatan=SelectField('Kecamatan', choices=[], validators=[DataRequired()])
    akreditas=SelectField('Akreditas', choices=[], validators=[DataRequired()])
    jenis_sekolah = SelectField('Jenis Sekolah', choices=[('Swasta','Swasta'),('Negri','Negeri')],validators=[DataRequired()])
    nama_kepsek=StringField('Nama Kepala Sekolah', validators=[DataRequired()])
    foto=FileField('Foto Sekolah', validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Tambah')

class data_sekolahedit(FlaskForm):
    npsn=StringField('NPSN', validators=[DataRequired()])
    nama_sekolah=StringField('Nama Kesatuan', validators=[DataRequired()])
    alamat=StringField('Desa/Kelurahan', validators=[DataRequired()])
    kecamatan=SelectField('Kecamatan', choices=[], validators=[DataRequired()])
    akreditas=SelectField('Akreditas', choices=[], validators=[DataRequired()])
    jenis_sekolah = SelectField('Jenis Sekolah', choices=[('Swasta','Swasta'),('Negri','Negeri')],validators=[DataRequired()])
    nama_kepsek=StringField('Nama Kepala Sekolah', validators=[DataRequired()])
    foto=FileField('Foto Sekolah', validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Simpan')
    
class akreditas_sekolah(FlaskForm):
    jenis_akreditas=StringField('Jenis Akreditas', validators=[DataRequired()])
    informasi_akreditas=TextAreaField('Informasi Akreditas')
    submit=SubmitField('Tambah')

class akreditas_sekolahedit(FlaskForm):
    jenis_akreditas=StringField('Jenis Akreditas', validators=[DataRequired()])
    informasi_akreditas=TextAreaField('Informasi Akreditas')
    submit=SubmitField('Simpan')

class kecamatan_sekolah(FlaskForm):
    jenis_wilayah=StringField('Jenis kecamatan', validators=[DataRequired()])
    informasi_wilayah=TextAreaField('Informasi Wilayah')
    submit=SubmitField('Tambah')

class kecamatan_sekolahedit(FlaskForm):
    jenis_wilayah=StringField('Jenis kecamatan', validators=[DataRequired()])
    informasi_wilayah=TextAreaField('Informasi Wilayah')
    submit=SubmitField('Simpan')

class pengaduan_F(FlaskForm):
    username = StringField('Subjek', validators=[DataRequired(),Length(min=10, max=15)])
    kategori = SelectField('Kategori Pengaduan', choices=[('Administrasi','Pelayanan Administrasi'),('fasilitas','Fasilitas'),('Efisiensi','Efisiensi')],validators=[DataRequired()])
    detail_pengaduan= TextAreaField('Pengaduan', validators=[DataRequired()])
    submit=SubmitField('Kirim')
    


class df_admin(FlaskForm):
    nama=StringField('Nama', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired(),Length(min=6, max=20)])
    konf_pass=PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    foto=FileField('Foto Sekolah', validators=[FileAllowed(['jpg','png'])])
    simpan=SubmitField('Tambah')

    def validate_email(self, email):
            cekemail=Tadmin.query.filter_by(email=email.data).first()
            if cekemail:
                raise ValidationError('Email Sudah Terdaftar, Gunakan Email Yang Lain')

class daftar_admin(FlaskForm):
    nama=StringField('Nama', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired(),Length(min=6, max=20)])
    konf_pass=PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    foto=FileField('Foto Sekolah', validators=[FileAllowed(['jpg','png'])])
    simpan=SubmitField('Tambah')

    def validate_email(self, email):
            cekemail=Tadmin.query.filter_by(email=email.data).first()
            if cekemail:
                raise ValidationError('Email Sudah Terdaftar, Gunakan Email Yang Lain')


class edit_admin(FlaskForm):
    nama=StringField('Nama', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired(),Length(min=6, max=20)])
    konf_pass=PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    foto=FileField('Foto Sekolah', validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Tambah')

    def validate_email(self, email):
        if email.data !=current_user.email:
            cekemail=Tadmin.query.filter_by(email=email.data).first()
            if cekemail:
                raise ValidationError('Email Sudah Terdaftar, Gunakan Email Yang Lain')

class login_admin(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired(),Length(min=6, max=20)])
    submit=SubmitField('Login')

class kegiatan_F(FlaskForm):
    tahun=StringField('Tahun', validators=[DataRequired()])
    judul=StringField('Judul', validators=[DataRequired()])
    program=StringField('Program', validators=[DataRequired()])
    bidang=SelectField('Bidang', choices=[('Sarana Prasaran','Sarana Prasarana'),('Kurikulum & Kesiswaan','Kurikulum & Kesiswaan'),('Mutu Guru & tenaga pendidikan','Mutu Guru & tenaga pendidikan')],validators=[DataRequired()])
    status=SelectField('Status', choices=[('Belum Terlaksana','Belum Terlaksana'),('Dalam Proses','Dalam Proses'),('Sudah Terlaksana','Sudah Terlaksana')],validators=[DataRequired()])
    submit=SubmitField('Simpan')

class kegiatan_edit(FlaskForm):
    tahun=StringField('Tahun', validators=[DataRequired()])
    judul=StringField('Judul', validators=[DataRequired()])
    program=StringField('Program', validators=[DataRequired()])
    bidang=SelectField('Bidang', choices=[('Sarana Prasaran','Sarana Prasarana'),('Kurikulum & Kesiswaan','Kurikulum & Kesiswaan'),('Mutu Guru & tenaga pendidikan','Mutu Guru & tenaga pendidikan')],validators=[DataRequired()])
    status=SelectField('Status', choices=[('Belum Terlaksana','Belum Terlaksana'),('Dalam Proses','Dalam Proses'),('Sudah Terlaksana','Sudah Terlaksana')],validators=[DataRequired()])
    submit=SubmitField('Simpan')

class informasi_F(FlaskForm):
    judul=StringField('Judul Informasi', validators=[DataRequired()])
    informasi= TextAreaField('Informasi')
    submit=SubmitField('Simpan')

class informasi_edit(FlaskForm):
    judul=StringField('Judul Informasi', validators=[DataRequired()])
    informasi= TextAreaField('Informasi')
    submit=SubmitField('Simpan')

class filter_dtumumm(FlaskForm):
    tahun=StringField('Tahun', validators=[DataRequired()])
    submit=SubmitField('Simpan')

class filter_dtumum(FlaskForm):
    tahun=StringField('Tahun', validators=[DataRequired()])
    submit=SubmitField('Simpan')