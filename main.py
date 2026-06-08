import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from moviepy.editor import AudioFileClip, ImageClip

# التوكن سيتم قراءته بأمان من إعدادات السيرفر المتقدمة
TOKEN = os.getenv("8955513084:AAEVZ5ydzCciSCvv1lLxw15wHMPt5nSdhoM")
BACKGROUND_IMAGE = "background.jpg" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! أرسل لي أي ملف صوتي وسأقوم بتحويله إلى فيديو بخلفية ثابتة فوراً.")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio_file = await update.message.audio.get_file() if update.message.audio else await update.message.voice.get_file()
    await update.message.reply_text("جاري معالجة الصوت وصناعة الفيديو... انتظر قليلاً ⏳")
    
    audio_path = "input_audio.ogg"
    await audio_file.download_to_drive(audio_path)
    output_video = "output_video.mp4"
    
    try:
        audio_clip = AudioFileClip(audio_path)
        video_clip = ImageClip(BACKGROUND_IMAGE).set_duration(audio_clip.duration)
        video_clip = video_clip.set_audio(audio_clip)
        
        video_clip.write_videofile(
            output_video, fps=10, codec="libx264", audio_codec="aac", logger=None
        )
        
        audio_clip.close()
        video_clip.close()
        
        with open(output_video, 'rb') as video:
            await update.message.reply_video(video=video, caption="تفضل، تم تحويل الصوت إلى فيديو بنجاح! 🎬")
            
    except Exception as e:
        await update.message.reply_text("عذراً، حدث خطأ أثناء تحويل الملف.")
    
    finally:
        await asyncio.sleep(1)
        if os.path.exists(audio_path): os.remove(audio_path)
        if os.path.exists(output_video): os.remove(output_video)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
    app.run_polling()

if __name__ == "__main__":
    main()
