from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from sim.models import Tprofil, Tdataumum, Tdatasekolah, Takresklh, Tkecamatan, Tpengaduan, Tadmin, Tberita

class pengaduan_F(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length(min=10, max=100)])
    kategori = SelectField(u'Kategori Pengaduan', choices=[('Administrasi','Pelayanan Administrasi'),('fasilitas','Fasilitas')],validators=[DataRequired()])
    detail_pengaduan= TextAreaField('Pengaduan', validators=[DataRequired()])
    submit=SubmitField('Kirimkan Pengaduan')

    def validate_email(self, email):
        if email.data !=email:
            cekemail=Tpengaduan.query.filter_by(email=email.data).first()
            if cekemail:
                raise ValidationError('Email Sudah Terdaftar, Gunakan Email Yang Lain')

class editpengaduan_F(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length(min=10, max=15)])
    kategori = SelectField('Kategori Pengaduan', choices=[('Administrasi','Pelayanan Administrasi'),('fasilitas','Fasilitas')],validators=[DataRequired()])
    detail_pengaduan= TextAreaField('Pengaduan', validators=[DataRequired()])
    submit=SubmitField("Ubah")