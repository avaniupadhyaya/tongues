import sqlite3
from datetime import datetime, timedelta

DATABASE = 'tongues.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proverbs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT NOT NULL,
            script TEXT NOT NULL,
            romanised TEXT,
            literal_translation TEXT,
            real_meaning TEXT NOT NULL,
            english_equivalent TEXT,
            notes TEXT,
            verified BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proverb_equivalents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proverb_id INTEGER NOT NULL,
            target_language TEXT NOT NULL,
            equivalent_script TEXT NOT NULL,
            equivalent_romanised TEXT,
            FOREIGN KEY (proverb_id) REFERENCES proverbs(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_lang TEXT NOT NULL,
            target_lang TEXT NOT NULL,
            input_text TEXT NOT NULL,
            translation TEXT NOT NULL,
            rating TEXT NOT NULL,
            comment TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_lang TEXT NOT NULL,
            target_lang TEXT NOT NULL,
            input_length INTEGER,
            success BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('SELECT COUNT(*) as total FROM proverbs')
    count = cursor.fetchone()['total']

    if count == 0:
        proverbs = [
            # ── GUJARATI (100) ──
            ('Gujarati', 'ક્રિયા શબ્દો કરતાં મોટેથી બોલે છે', 'Kriya shabdo karta mothetha bole chhe', 'Actions speak louder than words', 'What people do matters more than what they say', 'Actions speak louder than words', None),
            ('Gujarati', 'સમયસર લીધેલ ટાંકો નવ ટાંકા બચાવે છે', 'Samaysar lidhe tanko nav tanka bachave chhe', 'A stitch in time saves nine', 'Fixing a small problem early prevents bigger trouble', 'A stitch in time saves nine', None),
            ('Gujarati', 'મોડા કરતાં ક્યારેય નહીં', 'Moda karta kyarey nahi', 'Better late than never', 'Doing something late is better than not at all', 'Better late than never', None),
            ('Gujarati', 'અભ્યાસ પરિપૂર્ણ બનાવે છે', 'Abhyas paripurna banave chhe', 'Practice makes perfect', 'Repeated effort leads to mastery', 'Practice makes perfect', None),
            ('Gujarati', 'જ્યાં ઇચ્છા ત્યાં માર્ગ', 'Jyaan ichchha tyaan maarg', 'Where there is a will there is a way', 'Strong determination finds a path forward', 'Where there is a will there is a way', None),
            ('Gujarati', 'વહેલો પક્ષી કીડો પકડે છે', 'Vahelo pakshi keedo pakde chhe', 'The early bird catches the worm', 'Those who start early get the best opportunities', 'The early bird catches the worm', None),
            ('Gujarati', 'પ્રામાણિકતા શ્રેષ્ઠ નીતિ છે', 'Pramanikta shrestha niti chhe', 'Honesty is the best policy', 'Being truthful always leads to better outcomes', 'Honesty is the best policy', None),
            ('Gujarati', 'કૂદતા પહેલા જુઓ', 'Koodata pahela juo', 'Look before you leap', 'Think carefully before taking action', 'Look before you leap', None),
            ('Gujarati', 'બે માથા એક કરતાં સારા', 'Be matha ek karta saara', 'Two heads are better than one', 'Collaboration leads to better results', 'Two heads are better than one', None),
            ('Gujarati', 'પુસ્તકને તેના આવરણ પરથી ન આંકો', 'Pustakne tena aavaran parathi na aanko', 'Do not judge a book by its cover', 'Do not judge something by its appearance alone', "Don't judge a book by its cover", None),
            ('Gujarati', 'દરેક વાદળને ચાંદીની કિનારી હોય છે', 'Darek vaadalne chandini kinari hoy chhe', 'Every cloud has a silver lining', 'There is something positive in every difficult situation', 'Every cloud has a silver lining', None),
            ('Gujarati', 'જે ચળકે છે તે બધું સોનું નથી', 'Je chalake chhe te badhu sonu nathi', 'All that glitters is not gold', 'Appearances can be deceptive', 'All that glitters is not gold', None),
            ('Gujarati', 'એક જ પીંછાના પક્ષીઓ સાથે ઊડે છે', 'Ek j pichhaana pakshio sathe ude chhe', 'Birds of a feather flock together', 'People with similar interests gather together', 'Birds of a feather flock together', None),
            ('Gujarati', 'નસીબ હિંમતવાળાનો સાથ આપે છે', 'Nasib himmatvaalano saath aape chhe', 'Fortune favors the bold', 'Brave and decisive people get better opportunities', 'Fortune favors the bold', None),
            ('Gujarati', 'સમય એ પૈસો છે', 'Samay e paiso chhe', 'Time is money', 'Time is as valuable as money and should not be wasted', 'Time is money', None),
            ('Gujarati', 'જરૂરિયાત શોધનો આધાર છે', 'Jaruryat shodh no aadhaar chhe', 'Necessity is the mother of invention', 'Problems and needs push people to find solutions', 'Necessity is the mother of invention', None),
            ('Gujarati', 'ઘણા રસોઈયા ખીચડી બગાડે છે', 'Ghana rasoia khichdi bagade chhe', 'Too many cooks spoil the broth', 'Too many people involved in something causes problems', 'Too many cooks spoil the broth', None),
            ('Gujarati', 'કષ્ટ વિના ફળ નહીં', 'Kasht vina fal nahi', 'No pain no gain', 'You cannot achieve anything without effort', 'No pain no gain', None),
            ('Gujarati', 'સહેલાઈથી આવ્યું સહેલાઈથી જાય', 'Sahelaaithi aavyu sahelaaithi jaay', 'Easy come easy go', 'Things obtained without effort are lost just as easily', 'Easy come easy go', None),
            ('Gujarati', 'એક ચિત્ર હજાર શબ્દો જેટલું છે', 'Ek chitra hazar shabdo jetlu chhe', 'A picture is worth a thousand words', 'A visual conveys more meaning than words alone', 'A picture is worth a thousand words', None),
            ('Gujarati', 'ધીમો અને સ્થિર દોડ જીતે છે', 'Dhimo ane sthir dod jite chhe', 'Slow and steady wins the race', 'Consistent effort beats rushing and carelessness', 'Slow and steady wins the race', None),
            ('Gujarati', 'ભિખારીઓ પસંદ ન કરી શકે', 'Bhikhariao pasand na kari shake', 'Beggars cannot be choosers', 'Those in need must accept what is available', 'Beggars cannot be choosers', None),
            ('Gujarati', 'જેવું વાવો તેવું લણો', 'Jevu vaavo tevu lano', 'You reap what you sow', 'Your actions determine your outcomes', 'You reap what you sow', None),
            ('Gujarati', 'કલમ તલવાર કરતાં વધુ શક્તિશાળી છે', 'Kalam talvar karta vadhu shaktishaali chhe', 'The pen is mightier than the sword', 'Words and ideas are more powerful than force', 'The pen is mightier than the sword', None),
            ('Gujarati', 'શ્રેષ્ઠ માટે આશા રાખો સૌથી ખરાબ માટે તૈયાર રહો', 'Shrestha maate asha rakho sauthi kharaab maate taiyaar raho', 'Hope for the best prepare for the worst', 'Be optimistic but also prepared for difficulties', 'Hope for the best prepare for the worst', None),
            ('Gujarati', 'રોમમાં રોમનો જેવું કરો', 'Rom ma Romano jevu karo', 'When in Rome do as the Romans do', 'Adapt to local customs wherever you go', 'When in Rome do as the Romans do', None),
            ('Gujarati', 'જેવી દ્રષ્ટિ તેવી સૃષ્ટિ', 'Jevi drashti tevi srushti', 'As the vision so the world', 'Beauty and perception lie in the eyes of the observer', 'Beauty is in the eye of the beholder', None),
            ('Gujarati', 'સ્વચ્છતા ઈશ્વરભક્તિ પછી આવે છે', 'Swachhhata Ishvarbhakti pachhi aave chhe', 'Cleanliness is next to godliness', 'Being clean is a moral and spiritual virtue', 'Cleanliness is next to godliness', None),
            ('Gujarati', 'જે હાથ તમને ખવડાવે તેને ન કરડો', 'Je haath tamne khavadaave tene na karado', 'Do not bite the hand that feeds you', 'Do not harm those who help or support you', "Don't bite the hand that feeds you", None),
            ('Gujarati', 'બધા ઈંડા એક ટોપલીમાં ન મૂકો', 'Badha inda ek topali ma na muko', 'Do not put all your eggs in one basket', 'Do not risk everything on a single option', "Don't put all your eggs in one basket", None),
            ('Gujarati', 'મહાન મન એક સરખું વિચારે છે', 'Mahaan man ek sarkhu vichare chhe', 'Great minds think alike', 'Intelligent people often come to the same conclusions', 'Great minds think alike', None),
            ('Gujarati', 'જ્ઞાન એ શક્તિ છે', 'Dnyan e shakti chhe', 'Knowledge is power', 'Having knowledge gives you advantage and influence', 'Knowledge is power', None),
            ('Gujarati', 'હાસ્ય શ્રેષ્ઠ દવા છે', 'Haaasyu shrestha dava chhe', 'Laughter is the best medicine', 'Joy and humour heal both body and mind', 'Laughter is the best medicine', None),
            ('Gujarati', 'પૈસા ઝાડ પર ઊગતા નથી', 'Paisa zaad par ugta nathi', 'Money does not grow on trees', 'Money must be earned through hard work', "Money doesn't grow on trees", None),
            ('Gujarati', 'કોઈ સમાચાર નહીં એ સારા સમાચાર છે', 'Koi samachar nahi e saara samachar chhe', 'No news is good news', 'Lack of news usually means things are going fine', 'No news is good news', None),
            ('Gujarati', 'જૂનું સોનું છે', 'Juunu sonu chhe', 'Old is gold', 'Old things and traditions often have great value', 'Old is gold', None),
            ('Gujarati', 'એક ભલાઈ બીજી ભલાઈ ને લાયક છે', 'Ek bhalai biji bhalai ne laayak chhe', 'One good turn deserves another', 'Kindness should be reciprocated', 'One good turn deserves another', None),
            ('Gujarati', 'નજર બહાર મન બહાર', 'Najar bahar man bahar', 'Out of sight out of mind', 'People forget things or people they cannot see', 'Out of sight out of mind', None),
            ('Gujarati', 'જે ઉપદેશ આપો તે પ્રમાણે ચાલો', 'Je updesh aapo te pramane chalo', 'Practice what you preach', 'Act according to the advice you give to others', 'Practice what you preach', None),
            ('Gujarati', 'રોમ એક દિવસમાં બન્યું નહોતું', 'Rom ek divas ma banyu nahotu', 'Rome was not built in a day', 'Great achievements take time and sustained effort', "Rome wasn't built in a day", None),
            ('Gujarati', 'જોવું એ માનવું છે', 'Jovu e maanvu chhe', 'Seeing is believing', 'People believe what they can observe with their own eyes', 'Seeing is believing', None),
            ('Gujarati', 'લોઢું ગરમ હોય ત્યારે ઘા મારો', 'Lodhu garam hoy tyaare ghaa maaro', 'Strike while the iron is hot', 'Take advantage of an opportunity while it exists', 'Strike while the iron is hot', None),
            ('Gujarati', 'બીજી બાજુનું ઘાસ હંમેશા લીલું હોય છે', 'Biji baaju nu ghaas hamesha lilu hoy chhe', 'The grass is always greener on the other side', 'People always think others have it better', 'The grass is always greener on the other side', None),
            ('Gujarati', 'ઘર જેવી કોઈ જગ્યા નથી', 'Ghar jevi koi jagya nathi', 'There is no place like home', 'Home is the most comfortable and beloved place', 'There is no place like home', None),
            ('Gujarati', 'અતિ સર્વત્ર વર્જયેત', 'Ati sarvatra varjayet', 'Excess should be avoided everywhere', 'Too much of anything is harmful', 'Too much of anything is bad', 'Sanskrit origin widely used in Gujarati'),
            ('Gujarati', 'સત્ય કાલ્પનિક કરતાં વિચિત્ર છે', 'Satya kalpanic karta vichitra chhe', 'Truth is stranger than fiction', 'Real life events are often more surprising than stories', 'Truth is stranger than fiction', None),
            ('Gujarati', 'સાથે ઊભા રહીએ તો જીતીએ', 'Sathe ubha rahie to jitie', 'United we stand divided we fall', 'Unity brings strength while division leads to defeat', 'United we stand divided we fall', None),
            ('Gujarati', 'વૈવિધ્ય જીવનનો મસાલો છે', 'Vaividhya jivannoo masalo chhe', 'Variety is the spice of life', 'Differences and new experiences make life interesting', 'Variety is the spice of life', None),
            ('Gujarati', 'સારી શરૂઆત અડધું કામ છે', 'Saari shuruat addhu kaam chhe', 'Well begun is half done', 'A good start makes the rest of the work much easier', 'Well begun is half done', None),
            ('Gujarati', 'ટીપે ટીપે સરોવર ભરાય', 'Tipe tipe sarovar bharay', 'Drop by drop a lake fills up', 'Small consistent efforts lead to great results', 'Every little bit counts', None),
            ('Gujarati', 'દૂધનો દાઝેલો છાશ પણ ફૂંકી ફૂંકીને પીએ', 'Dudh no daazelo chaash pan funki funkine piye', 'One burned by milk blows even on buttermilk', 'Once hurt a person becomes overly cautious', 'Once bitten twice shy', 'Very commonly used in Gujarati households'),
            ('Gujarati', 'નાચ ન જાણે આંગણ વાંકુ', 'Naach na jaane aangan vaanku', 'Cannot dance so blames the courtyard', 'A bad workman blames their tools or circumstances', 'A bad workman blames his tools', None),
            ('Gujarati', 'ઘરનો વૈદ્ય ગધેડો', 'Gharna vaidya gadhedo', 'The doctor at home is a donkey', 'Expertise is not valued when it comes from someone close to you', 'A prophet is not recognised in his own land', None),
            ('Gujarati', 'સો સોનાર ની એક લુહાર ની', 'So sonar ni ek luhar ni', 'A hundred blows of a goldsmith equal one of a blacksmith', 'One decisive action is worth more than many weak attempts', 'One decisive blow beats a hundred light ones', None),
            ('Gujarati', 'આંધળામાં કાણો રાજા', 'Aandhla ma kaano raja', 'Among the blind the one-eyed is king', 'Even partial ability makes you stand out', 'In the land of the blind the one-eyed man is king', None),
            ('Gujarati', 'મૂળ કરતા વ્યાજ વહાલું', 'Mool karta vyaaj vahalu', 'The interest is dearer than the principal', 'Grandparents love their grandchildren even more than their own children', 'Grandparents always cherish their grandchildren more than their own children', 'About family love NOT finance'),
            ('Gujarati', 'દૂરથી ડુંગર રળિયામણા', 'Durathi dungar radiyamna', 'Mountains look beautiful from afar', 'Things seem more appealing from a distance than they really are', 'The grass is always greener on the other side', None),
            ('Gujarati', 'જ્યાં ચાહ ત્યાં રાહ', 'Jyaan chaah tyaan raah', 'Where there is will there is a way', 'Determination always finds a path', 'Where there is a will there is a way', None),
            ('Gujarati', 'એક હાથે તાળી ન પડે', 'Ek haathe taali na pade', 'One hand cannot clap', 'Nothing worthwhile is achieved alone', 'It takes two to tango', None),
            ('Gujarati', 'ઉતાવળે આંબા ન પાકે', 'Utavle aamba na paake', 'Hurrying will not ripen mangoes', 'Rushing does not speed up natural processes', "Rome wasn't built in a day", None),
            ('Gujarati', 'ઘરની મરઘી દાળ બરાબર', 'Gharni marghi daal barabar', 'The hen at home is worth only dal', 'Familiarity makes people undervalue what they have', 'Familiarity breeds contempt', None),
            ('Gujarati', 'બાર ગાઉએ બોલી બદલાય', 'Baar gaue boli badle', 'Speech changes every twelve miles', 'Language and culture shift constantly across regions', None, 'Reflects Gujarati linguistic diversity'),
            ('Gujarati', 'સંગ તેવો રંગ', 'Sang tevo rang', 'You take on the colour of your company', 'You become like the people you spend time with', 'You are known by the company you keep', None),
            ('Gujarati', 'ભૂખ્યા ભજન ન થાય', 'Bhukha bhajan na thaay', 'A hungry person cannot do devotion', 'Basic needs must be met before higher goals can be pursued', 'An empty stomach cannot focus on higher things', None),
            ('Gujarati', 'જેની લાઠી તેની ભેંસ', 'Jeni laathi teni bhens', 'Whoever has the stick owns the buffalo', 'Power and strength determine who controls resources', 'Might is right', None),
            ('Gujarati', 'ધૈર્ય ફળ આપે છે', 'Dhairy fal aape chhe', 'Patience bears fruit', 'Good things come to those who wait with patience', 'Patience is a virtue', None),
            ('Gujarati', 'ન બોલ્યામાં નવ ગુણ', 'Na bolya ma nav gun', 'In not speaking there are nine virtues', 'Silence is often wiser than unnecessary talk', 'Speech is silver silence is gold', None),
            ('Gujarati', 'ખાડો ખોદે તે પડે', 'Khaado khode te pade', 'Whoever digs a pit falls into it', 'Those who scheme against others suffer the same fate', 'He who digs a pit for others falls in himself', None),
            ('Gujarati', 'સાચું બોલો ડરો ના', 'Sachu bolo daro na', 'Speak truth and fear not', 'Honesty requires courage but it is always the right path', 'The truth shall set you free', None),
            ('Gujarati', 'ઢોળ ઢળ્યા પછી ડૂચો', 'Dhol dhalya pachhi ducho', 'Cleaning up after the spill', 'It is too late to act after the damage is done', 'No use crying over spilled milk', None),
            ('Gujarati', 'ડૂબતો ઝાંઝવાં ઝાલે', 'Dubto zaanzva zaale', 'A drowning person grasps at mirages', 'A desperate person will try anything even hopeless options', 'A drowning man clutches at a straw', None),
            ('Gujarati', 'ખાધું પીધું ને વહ્યું ગયું', 'Khadhu pidhu ne vahyu gayu', 'Ate drank and it all flowed away', 'Enjoyment without saving leads to nothing lasting', 'Easy come easy go', None),
            ('Gujarati', 'ડહાપણ ઉંમર સાથે આવે', 'Dahapan ummar sathe aave', 'Wisdom comes with age', 'Experience and years bring greater understanding', 'Wisdom comes with age', None),
            ('Gujarati', 'માણસ પારખ્યા વિના ન ઓળખાય', 'Maanas paarakhya vina na olakhay', 'A person cannot be known without testing', 'You only truly know someone when they face difficulty', 'Adversity reveals character', None),
            ('Gujarati', 'અનુભવ શ્રેષ્ઠ શિક્ષક છે', 'Anubhav shrestha shikshak chhe', 'Experience is the best teacher', 'Learning from real life is the most powerful education', 'Experience is the best teacher', None),
            ('Gujarati', 'ઉમ્મીદ પર દુનિયા ટકી છે', 'Ummid par duniya taki chhe', 'The world stands on hope', 'Hope sustains people through all hardships', 'Hope springs eternal', None),
            ('Gujarati', 'ઊંટ ની ઘૂંટ', 'Unt ni ghunt', 'A sip for a camel', 'An amount so small it barely makes a difference', 'A drop in the ocean', None),
            ('Gujarati', 'ભેગા મળીએ ભાર ઓછો', 'Bhega malie bhaar ochho', 'When together the burden is lighter', 'Shared effort makes hard tasks easier', 'Many hands make light work', None),
            ('Gujarati', 'એકલો જઈ ન શકાય', 'Ekalo jai na shakay', 'One cannot go alone', 'Some goals require companionship and teamwork', 'No man is an island', None),
            ('Gujarati', 'પ્રેમ અને ઉધારો છુપાવ્યા ન છૂપે', 'Prem ane udhaaro chhupavya na chhupe', 'Love and debt cannot be hidden', 'True feelings and obligations always reveal themselves', 'Love will find a way', None),
            ('Gujarati', 'ઓછા ભણ્યા ઘણા ગણ્યા', 'Ochha bhanya ghana ganya', 'Less educated but highly counted', 'Practical wisdom matters more than formal education alone', 'Common sense is not so common', None),
            ('Gujarati', 'વડ ત્યાં છાંયો', 'Vad tyaan chhaayo', 'Where there is a banyan tree there is shade', 'A powerful protector provides shelter to those around them', 'A great person provides for those around them', None),
            ('Gujarati', 'ઘરમાં ઘૂઘરા બહાર ભૂખ', 'Ghar ma ghughara bahar bhukh', 'Bells at home hunger outside', 'Those who appear prosperous may struggle privately', 'All that glitters is not gold', None),
            ('Gujarati', 'ઉગ્યો ત્યારથી ઊગ્યો', 'Ugyo tyaarthi ugyo', 'It starts growing from when it first sprouts', 'Character formed early shapes the whole life', 'As the twig is bent so grows the tree', None),

            ('Gujarati', 'ઘડ્યો ઘડ્યો ઘડો ફૂટ્યો', 'Ghadyo ghadyo ghado futo', 'A carefully made pot still breaks', 'Even well-made things can be destroyed carelessly', 'Handle with care', None),
            ('Gujarati', 'ફળ ન આવ્યા ત્યાં ફૂલ ન ઝરે', 'Fal na aavya tyaan ful na jhare', 'Where there is no fruit no flower falls', 'Without proper conditions results cannot happen', 'You cannot get blood from a stone', None),
            ('Gujarati', 'ભૂલ્યો ભટક્યો ઘેર આવ્યો', 'Bhulyo bhatakyo gher aavyo', 'The one who was lost came home', 'Even those who go astray can find their way back', 'All roads lead to home', None),
            ('Gujarati', 'ઓળખ ઓળખ ઓળખ', 'Olakh olakh olakh', 'Knowing knowing knowing', 'The right connections and recognition open doors', 'It is not what you know but who you know', None),
            ('Gujarati', 'ચોર ઘરે ચોર', 'Chor ghare chor', 'A thief in a thief s home', 'When dishonest people face dishonesty themselves', 'Set a thief to catch a thief', None),
            ('Gujarati', 'ઉડ ગઈ ચકલી ભરી ભૂખ', 'Ud gayi chakli bhari bhukh', 'The sparrow flew away still hungry', 'Sometimes opportunity is lost before you can grasp it', 'The bird has flown', None),
            ('Gujarati', 'ન ખાવ ન ખવડાવો', 'Na khaav na khavdaavo', 'Neither eat nor feed others', 'A miserly person who neither enjoys life nor helps others', 'Neither fish nor fowl', None),
            ('Gujarati', 'જ્ઞાની ને ઘેર જ્ઞાન', 'Dnyan-i ne gher dnyan', 'Wisdom resides in the home of the wise', 'Wise people create environments of learning', 'Wisdom attracts wisdom', None),
            ('Gujarati', 'ચોક્કસ ગ્રાહક ભૂખ્યો ન રહે', 'Chokkas graahak bhukho na rahe', 'A determined customer never stays hungry', 'Persistence and determination always get results', 'Fortune favors the bold', None),
            ('Gujarati', 'મેહનત નો રોટલો', 'Mehnat no rotlo', 'The bread of hard work', 'What you earn through effort is the most satisfying', 'Hard work pays off', None),
            ('Gujarati', 'સ્વાર્થ વિના સ્નેહ નહીં', 'Swaaarth vina sneha nahi', 'Without self-interest there is no affection', 'People often have ulterior motives even in friendship', 'There is no such thing as a free lunch', None),
            ('Gujarati', 'ઊઠ જાગ મુસાફર', 'Uth jaag musafar', 'Rise and wake traveller', 'Do not delay what needs to be done now', 'The early bird catches the worm', None),
            ('Gujarati', 'ઘરના ઘઉં ઘંટીમાં', 'Gharna ghau ghantima', 'Home wheat in the mill', 'Making use of what you already have at home', 'Charity begins at home', None),
            ('Gujarati', 'માણસ ખોટો ના હોય ભૂલ ખોટી હોય', 'Maanas khoto na hoy bhul khoti hoy', 'The person is not wrong the mistake is wrong', 'Separate the action from the person when judging', 'Hate the sin not the sinner', None),

            ('Gujarati', 'ઉત્સાહ ભારે ઓજાર', 'Utsaah bhaare ojar', 'Enthusiasm is a heavy tool', 'Passion and energy are powerful instruments for success', 'Enthusiasm moves the world', None),
            ('Gujarati', 'દિવા નીચે અંધારું', 'Diva niche andhaaru', 'Darkness under the lamp', 'Those closest to the source are often least aware of it', 'The cobbler s children have no shoes', None),

            # ── HINDI (100) ──
            ('Hindi', 'क्रियाएं शब्दों से ज़ोर से बोलती हैं', 'Kriyaen shabdon se zor se bolti hain', 'Actions speak louder than words', 'What people do matters more than what they say', 'Actions speak louder than words', None),
            ('Hindi', 'समय पर लिया टाँका नौ टाँके बचाता है', 'Samay par liya taanka nau taanke bachaata hai', 'A stitch in time saves nine', 'Fixing a small problem early prevents bigger trouble', 'A stitch in time saves nine', None),
            ('Hindi', 'देर आए दुरुस्त आए', 'Der aaye durust aaye', 'Late but correct arrival', 'Doing something late is better than not doing it at all', 'Better late than never', None),
            ('Hindi', 'करत करत अभ्यास के जड़मति होत सुजान', 'Karat karat abhyas ke jadmati hot sujan', 'With constant practice even a dull mind becomes sharp', 'Repeated effort leads to mastery', 'Practice makes perfect', None),
            ('Hindi', 'जहाँ चाह वहाँ राह', 'Jahan chaah wahaan raah', 'Where there is a will there is a way', 'Strong determination finds a path forward', 'Where there is a will there is a way', None),
            ('Hindi', 'सच बोलो डरो मत', 'Sach bolo daro mat', 'Speak truth fear not', 'Honesty requires courage but is always the right path', 'Honesty is the best policy', None),
            ('Hindi', 'पहले तोलो फिर बोलो', 'Pehle tolo phir bolo', 'First weigh then speak', 'Think carefully before taking any action', 'Look before you leap', None),
            ('Hindi', 'दो सिर एक से बेहतर हैं', 'Do sir ek se behtar hain', 'Two heads are better than one', 'Collaboration leads to better results', 'Two heads are better than one', None),
            ('Hindi', 'किताब को उसके आवरण से मत आँको', 'Kitaab ko uske aavaran se mat aanko', 'Do not judge a book by its cover', 'Do not judge something by its appearance alone', "Don't judge a book by its cover", None),
            ('Hindi', 'हर मुसीबत में कोई न कोई रास्ता होता है', 'Har musibat mein koi na koi raasta hota hai', 'In every difficulty there is some way out', 'There is something positive in every difficult situation', 'Every cloud has a silver lining', None),
            ('Hindi', 'सब जो चमकता है सोना नहीं होता', 'Sab jo chamakta hai sona nahi hota', 'Not everything that glitters is gold', 'Appearances can be deceptive', 'All that glitters is not gold', None),
            ('Hindi', 'एक जैसे पंछी साथ उड़ते हैं', 'Ek jaise panchhi saath udte hain', 'Birds of the same kind fly together', 'People with similar interests gather together', 'Birds of a feather flock together', None),
            ('Hindi', 'भाग्य बहादुरों का साथ देता है', 'Bhaagya bahaduron ka saath deta hai', 'Fortune accompanies the brave', 'Brave and decisive people get better opportunities', 'Fortune favors the bold', None),
            ('Hindi', 'समय ही धन है', 'Samay hi dhan hai', 'Time itself is wealth', 'Time is as valuable as money and should not be wasted', 'Time is money', None),
            ('Hindi', 'आवश्यकता आविष्कार की जननी है', 'Aavashyakta aavishkaar ki janani hai', 'Necessity is the mother of invention', 'Problems and needs push people to find solutions', 'Necessity is the mother of invention', None),
            ('Hindi', 'ज़्यादा रसोइए खिचड़ी बिगाड़ते हैं', 'Zyada rasoi-ye khichdi bigadte hain', 'Too many cooks ruin the khichdi', 'Too many people involved causes problems', 'Too many cooks spoil the broth', None),
            ('Hindi', 'बिना मेहनत के फल नहीं मिलता', 'Bina mehnat ke fal nahi milta', 'Without effort there is no fruit', 'You cannot achieve anything without hard work', 'No pain no gain', None),
            ('Hindi', 'आया गया चला गया', 'Aaya gaya chala gaya', 'Came went gone', 'Things obtained without effort are lost just as easily', 'Easy come easy go', None),
            ('Hindi', 'एक तस्वीर हजार शब्दों के बराबर है', 'Ek tasveer hazaar shabdon ke barabar hai', 'A picture equals a thousand words', 'A visual conveys more meaning than words alone', 'A picture is worth a thousand words', None),
            ('Hindi', 'धीरे धीरे रे मना धीरे सब कुछ होय', 'Dheere dheere re mana dheere sab kuch hoye', 'Slowly slowly dear mind everything happens slowly', 'Consistent effort beats rushing and carelessness', 'Slow and steady wins the race', None),
            ('Hindi', 'माँगने वाले को चुनने का अधिकार नहीं', 'Maangne waale ko chunne ka adhikar nahi', 'One who begs has no right to choose', 'Those in need must accept what is available', 'Beggars cannot be choosers', None),
            ('Hindi', 'जैसी करनी वैसी भरनी', 'Jaisi karni waisi bharni', 'As you do so shall you receive', 'Your actions determine your outcomes', 'You reap what you sow', None),
            ('Hindi', 'कलम तलवार से ज़्यादा ताकतवर है', 'Kalam talwar se zyada takatvar hai', 'The pen is more powerful than the sword', 'Words and ideas are more powerful than force', 'The pen is mightier than the sword', None),
            ('Hindi', 'अच्छे की उम्मीद रखो बुरे के लिए तैयार रहो', 'Achhe ki ummid rakho bure ke liye taiyaar raho', 'Keep hope for good be prepared for bad', 'Be optimistic but also prepared for difficulties', 'Hope for the best prepare for the worst', None),
            ('Hindi', 'जब रोम में होओ तो रोमन की तरह करो', 'Jab Rom mein ho to Roman ki tarah karo', 'When in Rome act like Romans', 'Adapt to local customs wherever you go', 'When in Rome do as the Romans do', None),
            ('Hindi', 'सुंदरता देखने वाले की आँखों में होती है', 'Sundarta dekhne wale ki aankhon mein hoti hai', 'Beauty lies in the eyes of the beholder', 'Beauty and perception lie in the eyes of the observer', 'Beauty is in the eye of the beholder', None),
            ('Hindi', 'सफाई भक्ति के बाद आती है', 'Safai bhakti ke baad aati hai', 'Cleanliness comes after devotion', 'Being clean is a moral and spiritual virtue', 'Cleanliness is next to godliness', None),
            ('Hindi', 'जो हाथ खिलाए उसे मत काटो', 'Jo haath khilaaye use mat kaato', 'Do not bite the hand that feeds you', 'Do not harm those who help or support you', "Don't bite the hand that feeds you", None),
            ('Hindi', 'सारे अंडे एक टोकरी में मत रखो', 'Saare ande ek tokri mein mat rakho', 'Do not put all eggs in one basket', 'Do not risk everything on a single option', "Don't put all your eggs in one basket", None),
            ('Hindi', 'बड़े दिमाग एक जैसा सोचते हैं', 'Bade dimaag ek jaisa sochte hain', 'Great minds think alike', 'Intelligent people often come to the same conclusions', 'Great minds think alike', None),
            ('Hindi', 'ज्ञान ही शक्ति है', 'Dnyan hi shakti hai', 'Knowledge itself is power', 'Having knowledge gives you advantage and influence', 'Knowledge is power', None),
            ('Hindi', 'हँसी सबसे अच्छी दवा है', 'Hansi sabse achhi dawa hai', 'Laughter is the best medicine', 'Joy and humour heal both body and mind', 'Laughter is the best medicine', None),
            ('Hindi', 'पैसा पेड़ पर नहीं उगता', 'Paisa ped par nahi ugta', 'Money does not grow on trees', 'Money must be earned through hard work', "Money doesn't grow on trees", None),
            ('Hindi', 'कोई खबर नहीं अच्छी खबर है', 'Koi khabar nahi achhi khabar hai', 'No news is good news', 'Lack of news usually means things are going fine', 'No news is good news', None),
            ('Hindi', 'पुराना सोना है', 'Purana sona hai', 'The old is gold', 'Old things and traditions often have great value', 'Old is gold', None),
            ('Hindi', 'एक भलाई दूसरी भलाई की हकदार है', 'Ek bhalai doosri bhalai ki haqdar hai', 'One good deed deserves another', 'Kindness should be reciprocated', 'One good turn deserves another', None),
            ('Hindi', 'आँखों से ओझल मन से दूर', 'Aankhon se ojhal man se door', 'Out of sight out of mind', 'People forget things or people they cannot see', 'Out of sight out of mind', None),
            ('Hindi', 'जो कहो वो करो', 'Jo kaho wo karo', 'Do what you say', 'Act according to the advice you give to others', 'Practice what you preach', None),
            ('Hindi', 'रोम एक दिन में नहीं बना था', 'Rom ek din mein nahi bana tha', 'Rome was not built in a day', 'Great achievements take time and sustained effort', "Rome wasn't built in a day", None),
            ('Hindi', 'देखना ही विश्वास है', 'Dekhna hi vishwas hai', 'Seeing itself is believing', 'People believe what they can observe', 'Seeing is believing', None),
            ('Hindi', 'लोहा गर्म हो तभी मारो', 'Loha garam ho tabhi maaro', 'Strike when the iron is hot', 'Take advantage of an opportunity while it exists', 'Strike while the iron is hot', None),
            ('Hindi', 'दूसरी तरफ की घास हमेशा हरी लगती है', 'Doosri taraf ki ghaas hamesha hari lagti hai', 'The grass on the other side always seems greener', 'People always think others have it better', 'The grass is always greener on the other side', None),
            ('Hindi', 'घर जैसी कोई जगह नहीं', 'Ghar jaisi koi jagah nahi', 'There is no place like home', 'Home is the most comfortable and beloved place', 'There is no place like home', None),
            ('Hindi', 'अति सर्वत्र वर्जयेत', 'Ati sarvatra varjayet', 'Excess should be avoided everywhere', 'Too much of anything is harmful', 'Too much of anything is bad', 'Sanskrit origin widely used'),
            ('Hindi', 'सच्चाई कल्पना से विचित्र होती है', 'Sachchai kalpana se vichitra hoti hai', 'Truth is stranger than fiction', 'Real events are often more surprising than stories', 'Truth is stranger than fiction', None),
            ('Hindi', 'एकता में बल है', 'Ekta mein bal hai', 'There is strength in unity', 'Unity brings strength while division leads to defeat', 'United we stand divided we fall', None),
            ('Hindi', 'विविधता जीवन का मसाला है', 'Vividhta jeevan ka masala hai', 'Variety is the spice of life', 'Differences and new experiences make life interesting', 'Variety is the spice of life', None),
            ('Hindi', 'अच्छी शुरुआत आधी सफलता है', 'Achhi shuruaat aadhi safalta hai', 'A good start is half the success', 'A good beginning makes the rest much easier', 'Well begun is half done', None),
            ('Hindi', 'अब पछताए होत क्या जब चिड़िया चुग गई खेत', 'Ab pachtaye hot kya jab chidiya chug gayi khet', 'What use is regret when the birds have eaten the field', 'It is too late to regret after the damage is done', 'No use crying over spilled milk', None),
            ('Hindi', 'बूंद बूंद से सागर भरता है', 'Bund bund se saagar bharta hai', 'Drop by drop the ocean fills', 'Small consistent efforts lead to great results', 'Every little bit counts', None),
            ('Hindi', 'दूध का जला छाछ भी फूंक फूंक कर पीता है', 'Dudh ka jala chaach bhi funky funk kar peeta hai', 'One burned by milk blows even on buttermilk', 'Once hurt a person becomes overly cautious', 'Once bitten twice shy', None),
            ('Hindi', 'नाच न जाने आंगन टेढ़ा', 'Naach na jaane aangan tedha', 'Cannot dance so blames the crooked courtyard', 'A bad workman blames their tools', 'A bad workman blames his tools', None),
            ('Hindi', 'घर का भेदी लंका ढाए', 'Ghar ka bhedi lanka dhaye', 'The insider who betrays can destroy Lanka', 'An insider betrayal causes the greatest damage', 'Beware the enemy within', None),
            ('Hindi', 'अंधों में काना राजा', 'Andhon mein kaana raja', 'Among the blind the one-eyed is king', 'Even partial ability makes you stand out', 'In the land of the blind the one-eyed man is king', None),
            ('Hindi', 'दूर के ढोल सुहावने', 'Door ke dhol suhavne', 'Distant drums sound sweet', 'Things seem more appealing from a distance than up close', 'The grass is always greener on the other side', None),
            ('Hindi', 'एक हाथ से ताली नहीं बजती', 'Ek haath se taali nahi bajti', 'One hand cannot clap', 'Nothing worthwhile is achieved alone', 'It takes two to tango', None),
            ('Hindi', 'सब्र का फल मीठा होता है', 'Sabr ka phal meetha hota hai', 'The fruit of patience is sweet', 'Good things come to those who wait', 'Patience is a virtue', None),
            ('Hindi', 'थोथा चना बाजे घना', 'Thotha chana baaje ghana', 'Empty chickpeas make the most noise', 'People with little substance talk the most', 'Empty vessels make the most noise', None),
            ('Hindi', 'खोदा पहाड़ निकली चुहिया', 'Khoda pahad nikli chuhiya', 'Dug a mountain out came a mouse', 'Enormous effort for a tiny result', 'Much ado about nothing', None),
            ('Hindi', 'बंदर क्या जाने अदरक का स्वाद', 'Bandar kya jaane adrak ka swaad', 'What does a monkey know of ginger', 'Something valuable is wasted on someone who cannot appreciate it', 'Pearls before swine', None),
            ('Hindi', 'जो गरजते हैं वो बरसते नहीं', 'Jo garajte hain wo baraste nahi', 'Those who thunder do not rain', 'People who talk a lot rarely deliver on their promises', 'Barking dogs seldom bite', None),
            ('Hindi', 'नौ दो ग्यारह होना', 'Nau do gyarah hona', 'Nine two eleven meaning to flee', 'To run away or escape from a situation quickly', 'To make a run for it', None),
            ('Hindi', 'उल्टा चोर कोतवाल को डाँटे', 'Ulta chor kotwal ko daante', 'The thief scolds the police officer', 'The wrongdoer accuses the innocent person', 'The pot calling the kettle black', None),
            ('Hindi', 'जान है तो जहान है', 'Jaan hai to jahaan hai', 'Where there is life there is the world', 'As long as you are alive there is always hope', 'While there is life there is hope', None),
            ('Hindi', 'अकेला चना भाड़ नहीं फोड़ सकता', 'Akela chana bhaad nahi phod sakta', 'A single chickpea cannot pop a roaster', 'One person alone cannot achieve big results', 'No man is an island', None),
            ('Hindi', 'आम के आम गुठलियों के दाम', 'Aam ke aam guthliyon ke daam', 'Profit from the mango and from its seed too', 'Getting double benefit from a single thing', 'Kill two birds with one stone', None),
            ('Hindi', 'अनुभव सबसे बड़ा शिक्षक है', 'Anubhav sabse bada shikshak hai', 'Experience is the greatest teacher', 'Learning from real life is the most powerful education', 'Experience is the best teacher', None),
            ('Hindi', 'हिम्मत-ए-मर्दां मदद-ए-खुदा', 'Himmat-e-mardan madad-e-Khuda', 'The courage of men is the help of God', 'God helps those who help themselves', 'God helps those who help themselves', None),
            ('Hindi', 'मन के हारे हार है मन के जीते जीत', 'Man ke haare haar hai man ke jeete jeet', 'Defeat lies in the mind victory lies in the mind', 'Your mindset determines whether you succeed or fail', 'Whether you think you can or cannot you are right', None),
            ('Hindi', 'जिसकी लाठी उसकी भैंस', 'Jiski laathi uski bhains', 'Whoever has the stick owns the buffalo', 'Power and strength determine who controls resources', 'Might is right', None),
            ('Hindi', 'दूरी दिल को बढ़ाती है', 'Doori dil ko badhaati hai', 'Distance grows the heart', 'Being apart makes feelings stronger', 'Absence makes the heart grow fonder', None),
            ('Hindi', 'ज्ञान बाँटने से बढ़ता है', 'Dnyan baantne se badhta hai', 'Knowledge grows by sharing', 'The more knowledge you share the more it spreads', 'Knowledge shared is knowledge multiplied', None),
            ('Hindi', 'परहेज़ इलाज से बेहतर है', 'Parheze ilaaj se behtar hai', 'Prevention is better than cure', 'It is better to avoid a problem than to fix it after', 'Prevention is better than cure', None),
            ('Hindi', 'लालच बुरी बला है', 'Laalach buri bala hai', 'Greed is a terrible affliction', 'Greed leads to downfall and suffering', 'Greed is the root of all evil', None),
            ('Hindi', 'मेहनत का फल मीठा होता है', 'Mehnat ka phal meetha hota hai', 'The fruit of hard work is sweet', 'Hard work always pays off with rewarding results', 'Hard work pays off', None),
            ('Hindi', 'सीखना कभी बंद नहीं होता', 'Seekhna kabhi band nahi hota', 'Learning never stops', 'There is always something new to learn at every age', 'Learning never ends', None),
            ('Hindi', 'दया करने से बड़ा धर्म नहीं', 'Daya karne se bada dharm nahi', 'There is no religion greater than compassion', 'Kindness and empathy are the highest virtues', 'Kindness costs nothing', None),
            ('Hindi', 'छोटे छोटे कदम बड़े बदलाव लाते हैं', 'Chhote chhote kadam bade badlaav laate hain', 'Small steps bring big changes', 'Gradual consistent effort creates major transformation', 'Small steps lead to big changes', None),
            ('Hindi', 'उम्र के साथ समझ आती है', 'Umra ke saath samajh aati hai', 'Understanding comes with age', 'Experience and years bring greater wisdom', 'Wisdom comes with age', None),
            ('Hindi', 'पानी में रहकर मगर से बैर नहीं', 'Paani mein rahkar magar se bair nahi', 'Living in water do not make enemies with the crocodile', 'Do not make enemies with those more powerful in their domain', 'Do not bite the hand that feeds you', None),
            ('Hindi', 'जो दिखता है वो बिकता है', 'Jo dikhta hai wo bikta hai', 'What is visible sells', 'Visibility and presentation matter enormously', 'Out of sight out of mind', None),
            ('Hindi', 'दिल से दिल की बात होती है', 'Dil se dil ki baat hoti hai', 'Heart speaks to heart', 'Genuine emotion connects people more than words', 'The heart knows what the heart wants', None),
            ('Hindi', 'जो बोया वो काटा', 'Jo boya wo kaata', 'What you planted you harvested', 'Consequences always follow actions', 'You reap what you sow', None),
            ('Hindi', 'बड़े बोल का सिर नीचा', 'Bade bol ka sir neeche', 'Big words lead to a bowed head', 'Boasting invites humiliation', 'Pride comes before a fall', None),
            ('Hindi', 'नेकी कर दरिया में डाल', 'Neki kar dariya mein daal', 'Do good and throw it in the river', 'Do good deeds without expecting anything in return', 'Virtue is its own reward', None),
            ('Hindi', 'सच्चाई परेशान होती है पर पराजित नहीं', 'Sachchai pareshan hoti hai par paraajit nahi', 'Truth is troubled but never defeated', 'The truth may be suppressed but it always prevails', 'Truth will out', None),
            ('Hindi', 'जल्दी का काम शैतान का', 'Jaldi ka kaam shaitan ka', 'Hasty work is the devil s work', 'Rushing leads to mistakes and poor results', 'Haste makes waste', None),
            ('Hindi', 'अपना हाथ जगन्नाथ', 'Apna haath Jagannath', 'Your own hand is Lord Jagannath', 'Self-reliance is the greatest strength', 'God helps those who help themselves', None),
            ('Hindi', 'घर का जोगी जोगड़ा आन गाँव का सिद्ध', 'Ghar ka jogi jogda aan gaon ka siddh', 'The local yogi is ordinary the outsider is a saint', 'Expertise is not valued when it comes from someone familiar', 'A prophet is not recognised in his own land', None),
            ('Hindi', 'काला अक्षर भैंस बराबर', 'Kaala akshar bhains barabar', 'Black letters are equal to a buffalo', 'Said of someone who cannot read or lacks basic knowledge', 'Ignorance is no excuse', None),
            ('Hindi', 'जो सोए उसे जगाओ जो जागे उसे सलाम', 'Jo soye use jagao jo jaage use salaam', 'Wake the sleeping salute the awake', 'Respect those who are already alert and striving', 'Fortune favors the prepared', None),
            ('Hindi', 'एक और एक ग्यारह होते हैं', 'Ek aur ek gyarah hote hain', 'One plus one makes eleven', 'Together people are far more powerful than alone', 'United we stand', None),
            ('Hindi', 'कोई काम छोटा नहीं होता', 'Koi kaam chhota nahi hota', 'No work is small', 'Every kind of work has its own dignity and value', 'All work is honorable', None),
            ('Hindi', 'जो बीत गई सो बात गई', 'Jo beet gayi so baat gayi', 'What has passed is past', 'Do not dwell on what cannot be changed', 'Let bygones be bygones', None),
            ('Hindi', 'बोया पेड़ बबूल का तो आम कहाँ से होय', 'Boya ped babool ka to aam kahaan se hoye', 'If you plant a thorn tree where will the mango come from', 'You cannot expect good results from bad actions', 'You reap what you sow', None),
            ('Hindi', 'हाथ कंगन को आरसी क्या', 'Haath kangan ko aarsi kya', 'Why a mirror to see the bracelet on your wrist', 'The obvious does not need proof or explanation', 'Seeing is believing', None),
            ('Hindi', 'चोर की दाढ़ी में तिनका', 'Chor ki daadhi mein tinka', 'There is a straw in the thief s beard', 'Guilty people are always nervous and give themselves away', 'Conscience makes cowards of us all', None),
            ('Hindi', 'न रहेगा बाँस न बजेगी बाँसुरी', 'Na rahega baans na bajegi baansuri', 'No bamboo no flute music', 'Remove the root cause and the problem disappears', 'No fuel no fire', None),
            ('Hindi', 'धोबी का कुत्ता न घर का न घाट का', 'Dhobi ka kutta na ghar ka na ghaat ka', 'The washerman s dog belongs neither to home nor riverside', 'Someone who fits in nowhere loses both worlds', 'Neither fish nor fowl', None),
            ('Hindi', 'दीपक तले अंधेरा', 'Deepak tale andhera', 'Darkness under the lamp', 'Those closest to the source are often least aware of it', 'The cobbler s children have no shoes', None),

            # ── MARATHI (100) ──
            ('Marathi', 'कृती शब्दांपेक्षा मोठ्याने बोलते', 'Kruti shabdaanpeksha mothyaane bolate', 'Actions speak louder than words', 'What people do matters more than what they say', 'Actions speak louder than words', None),
            ('Marathi', 'वेळेवर घेतलेली शिवण नऊ शिवणे वाचवते', 'Velevaar ghetleli shivan nau shivane waachavte', 'A stitch in time saves nine', 'Fixing a small problem early prevents bigger trouble', 'A stitch in time saves nine', None),
            ('Marathi', 'उशिरा आलो पण योग्य आलो', 'Ushira aalo pan yogya aalo', 'Came late but came correctly', 'Doing something late is better than not at all', 'Better late than never', None),
            ('Marathi', 'सराव माणसाला परिपूर्ण बनवतो', 'Saraav maansaala paripurna banavato', 'Practice makes a person perfect', 'Repeated effort leads to mastery', 'Practice makes perfect', None),
            ('Marathi', 'जिथे इच्छा तिथे मार्ग', 'Jithe ichchha tithe maarg', 'Where there is will there is a way', 'Strong determination finds a path forward', 'Where there is a will there is a way', None),
            ('Marathi', 'पहाटेचा पक्षी किडा पकडतो', 'Pahaateecha pakshi kida pakadato', 'The early morning bird catches the worm', 'Those who start early get the best opportunities', 'The early bird catches the worm', None),
            ('Marathi', 'प्रामाणिकपणा ही सर्वोत्तम नीती आहे', 'Praamaanikapana hi sarvottam niti aahe', 'Honesty is the best policy', 'Being truthful always leads to better outcomes', 'Honesty is the best policy', None),
            ('Marathi', 'उडी मारण्यापूर्वी पाहा', 'Udi maarnyapurvi paahaa', 'Look before you leap', 'Think carefully before taking action', 'Look before you leap', None),
            ('Marathi', 'दोन डोकी एकापेक्षा चांगली', 'Don doki ekaapeksha chhangli', 'Two heads are better than one', 'Collaboration leads to better results', 'Two heads are better than one', None),
            ('Marathi', 'पुस्तकाला त्याच्या मुखपृष्ठावरून ओळखू नका', 'Pustakaala tyachya mukhprushthaavrun olakhu naka', 'Do not judge a book by its cover', 'Do not judge something by its appearance alone', "Don't judge a book by its cover", None),
            ('Marathi', 'प्रत्येक ढगाला चांदीची किनार असते', 'Pratyek dhagaala chandichi kinaar asate', 'Every cloud has a silver lining', 'There is something positive in every difficult situation', 'Every cloud has a silver lining', None),
            ('Marathi', 'जे चमकते ते सोने नसते', 'Je chamakte te sone nasate', 'Not everything that glitters is gold', 'Appearances can be deceptive', 'All that glitters is not gold', None),
            ('Marathi', 'एकाच पंखाचे पक्षी एकत्र उडतात', 'Ekaach pankhache pakshi ekatra udataat', 'Birds of the same feather fly together', 'People with similar interests gather together', 'Birds of a feather flock together', None),
            ('Marathi', 'नशीब धाडसी लोकांना साथ देते', 'Nashib dhaadasi lokaanna saath dete', 'Fortune supports the brave', 'Brave and decisive people get better opportunities', 'Fortune favors the bold', None),
            ('Marathi', 'वेळ म्हणजे पैसा', 'Vel mhanje paisa', 'Time means money', 'Time is as valuable as money', 'Time is money', None),
            ('Marathi', 'गरज ही शोधाची आई आहे', 'Garaj hi shodhaachi aai aahe', 'Necessity is the mother of invention', 'Problems and needs push people to find solutions', 'Necessity is the mother of invention', None),
            ('Marathi', 'जास्त स्वयंपाकी खीर बिघडवतात', 'Jaast swayampaki kheer bighadawataat', 'Too many cooks ruin the kheer', 'Too many people involved causes problems', 'Too many cooks spoil the broth', None),
            ('Marathi', 'कष्टाशिवाय फळ नाही', 'Kashtaashivaay phal naahi', 'Without effort there is no fruit', 'You cannot achieve anything without hard work', 'No pain no gain', None),
            ('Marathi', 'सहज आले सहज गेले', 'Sahaj aale sahaj gele', 'Easily came easily went', 'Things obtained without effort are lost just as easily', 'Easy come easy go', None),
            ('Marathi', 'एक चित्र हजार शब्दांएवढे आहे', 'Ek chitra hazaar shabdaanewadhe aahe', 'A picture equals a thousand words', 'A visual conveys more meaning than words alone', 'A picture is worth a thousand words', None),
            ('Marathi', 'सावकाश आणि स्थिरतेने शर्यत जिंकते', 'Saavakaash aani sthiratene sharyat jinkate', 'Slowly and steadily wins the race', 'Consistent effort beats rushing and carelessness', 'Slow and steady wins the race', None),
            ('Marathi', 'भिकाऱ्यांना निवड करण्याचा अधिकार नाही', 'Bhikaaaryaanna nivad karnyacha adhikaar naahi', 'Beggars have no right to choose', 'Those in need must accept what is available', 'Beggars cannot be choosers', None),
            ('Marathi', 'जशी करणी तशी भरणी', 'Jashi karani tashi bharani', 'As you do so shall you receive', 'Your actions determine your outcomes', 'You reap what you sow', None),
            ('Marathi', 'लेखणी तलवारीपेक्षा बलवान आहे', 'Lekhani talwaaripeksha balawaan aahe', 'The pen is mightier than the sword', 'Words and ideas are more powerful than force', 'The pen is mightier than the sword', None),
            ('Marathi', 'चांगल्याची आशा ठेवा वाईटासाठी तयार राहा', 'Chhanglaychi aasha theva vaaytaasaathi tayaar raahaa', 'Hope for good be ready for bad', 'Be optimistic but also prepared for difficulties', 'Hope for the best prepare for the worst', None),
            ('Marathi', 'रोममध्ये रोमन सारखे वागा', 'Rommadhye Roman sarakhe vaagaa', 'In Rome behave like Romans', 'Adapt to local customs wherever you go', 'When in Rome do as the Romans do', None),
            ('Marathi', 'सौंदर्य पाहणाऱ्याच्या डोळ्यात असते', 'Saundary paahanaaryachya dolyaat asate', 'Beauty lies in the eyes of the beholder', 'Beauty and perception lie in the eyes of the observer', 'Beauty is in the eye of the beholder', None),
            ('Marathi', 'स्वच्छता देवभक्तीशेजारी आहे', 'Swachhhata devbhaktishejari aahe', 'Cleanliness is next to godliness', 'Being clean is a moral and spiritual virtue', 'Cleanliness is next to godliness', None),
            ('Marathi', 'जो हात भरवतो त्याला चावू नका', 'Jo haath bharawato tyaala chaawu nakaa', 'Do not bite the hand that feeds you', 'Do not harm those who help or support you', "Don't bite the hand that feeds you", None),
            ('Marathi', 'सर्व अंडी एका टोपलीत ठेवू नका', 'Sarv andi ekaa topliit thewu nakaa', 'Do not put all eggs in one basket', 'Do not risk everything on a single option', "Don't put all your eggs in one basket", None),
            ('Marathi', 'महान मन एकसारखाच विचार करतात', 'Mahaan man ekasaaraakhaach vichaar kartat', 'Great minds think alike', 'Intelligent people often come to the same conclusions', 'Great minds think alike', None),
            ('Marathi', 'ज्ञान म्हणजे शक्ती', 'Dnyan mhanje shakti', 'Knowledge means power', 'Having knowledge gives you advantage and influence', 'Knowledge is power', None),
            ('Marathi', 'हशी ही सर्वोत्तम औषध आहे', 'Hashi hi sarvottam aushadha aahe', 'Laughter is the best medicine', 'Joy and humour heal both body and mind', 'Laughter is the best medicine', None),
            ('Marathi', 'पैसे झाडावर उगवत नाहीत', 'Paise zhaadaavar ugawat naahit', 'Money does not grow on trees', 'Money must be earned through hard work', "Money doesn't grow on trees", None),
            ('Marathi', 'कोणतीही बातमी नाही म्हणजे चांगली बातमी', 'Konateehi baatami naahi mhanje chhaangli baatami', 'No news means good news', 'Lack of news usually means things are going fine', 'No news is good news', None),
            ('Marathi', 'जुने सोने आहे', 'June sone aahe', 'The old is gold', 'Old things and traditions often have great value', 'Old is gold', None),
            ('Marathi', 'एक चांगले कृत्य दुसऱ्याला पात्र ठरवते', 'Ek chhangle krutya dusaaryaala paatr tharawate', 'One good deed deserves another', 'Kindness should be reciprocated', 'One good turn deserves another', None),
            ('Marathi', 'दृष्टीआड सृष्टी', 'Drushti-aad srushti', 'Out of sight the world disappears', 'People forget things or people they cannot see', 'Out of sight out of mind', None),
            ('Marathi', 'जे सांगाल ते करा', 'Je saangaal te karaa', 'Do what you preach', 'Act according to the advice you give to others', 'Practice what you preach', None),
            ('Marathi', 'रोम एका दिवसात बांधले गेले नाही', 'Rom ekaa divasaat baandhale gele naahi', 'Rome was not built in a day', 'Great achievements take time and sustained effort', "Rome wasn't built in a day", None),
            ('Marathi', 'पाहणे म्हणजे विश्वास ठेवणे', 'Paahane mhanje vishwas thewane', 'Seeing means believing', 'People believe what they can observe', 'Seeing is believing', None),
            ('Marathi', 'लोखंड गरम असताना घाव घाला', 'Lokhanda garam asataanaa ghaaw ghaala', 'Strike when the iron is hot', 'Take advantage of an opportunity while it exists', 'Strike while the iron is hot', None),
            ('Marathi', 'दुरून डोंगर साजरे', 'Duroon dongar saajare', 'Mountains look beautiful from afar', 'Things seem more appealing from a distance than up close', 'The grass is always greener on the other side', 'Very commonly used Marathi proverb'),
            ('Marathi', 'घरासारखी कोणतीच जागा नाही', 'Gharasarikhi konatich jaagaa naahi', 'There is no place like home', 'Home is the most comfortable and beloved place', 'There is no place like home', None),
            ('Marathi', 'अति तिथे माती', 'Ati tithe maati', 'Where there is excess there is ruin', 'Too much of anything causes harm', 'Too much of anything is bad', None),
            ('Marathi', 'सत्य कल्पनेपेक्षा विचित्र असते', 'Satya kalpaneepeksha vichitra asate', 'Truth is stranger than fiction', 'Real events are often more surprising than stories', 'Truth is stranger than fiction', None),
            ('Marathi', 'एकी असेल तर बळ असेल', 'Eki asel tar bal asel', 'Where there is unity there is strength', 'Unity brings strength while division leads to defeat', 'United we stand divided we fall', None),
            ('Marathi', 'विविधता जीवनाचा मसाला आहे', 'Vividhata jivanacha masala aahe', 'Variety is the spice of life', 'Differences and new experiences make life interesting', 'Variety is the spice of life', None),
            ('Marathi', 'चांगली सुरुवात अर्धे काम', 'Chhangli suruvaat ardhe kaam', 'A good start is half the work', 'A good beginning makes the rest much easier', 'Well begun is half done', None),
            ('Marathi', 'थेंबे थेंबे तळे साचे', 'Theme theme tale saache', 'Drop by drop a pool gathers', 'Small consistent efforts lead to great results over time', 'Every little bit counts', None),
            ('Marathi', 'नाचता येईना अंगण वाकडे', 'Nachata yeina angan vakade', 'Cannot dance so blames the crooked courtyard', 'A bad workman blames their tools', 'A bad workman blames his tools', None),
            ('Marathi', 'शहाण्याला शब्द एक मूर्खाला लाख', 'Shahanyala shabda ek murkhala lakh', 'A wise person needs one word a fool needs a hundred thousand', 'Intelligent people understand quickly', 'A word to the wise is sufficient', None),
            ('Marathi', 'जसे बीज पेराल तसे उगवेल', 'Jase beej peral tase ugavel', 'As you sow so shall it grow', 'Your actions determine your outcomes', 'You reap what you sow', None),
            ('Marathi', 'घरचा भेदी लंका जाळी', 'Gharcha bhedi lanka jaali', 'The insider who betrays burns Lanka', 'An insider betrayal causes the greatest damage', 'Beware the enemy within', None),
            ('Marathi', 'एका हाताने टाळी वाजत नाही', 'Eka haatane taali vaajat naahi', 'One hand cannot clap', 'Nothing worthwhile is achieved alone', 'It takes two to tango', None),
            ('Marathi', 'उतावळा नवरा गुडघ्याला बाशिंग', 'Utavala navra gudghyala bashing', 'The hasty groom ties the turban on his knee', 'Rushing leads to mistakes and poor results', 'Haste makes waste', None),
            ('Marathi', 'बुडत्याला काडीचा आधार', 'Budatyala kaadicha aadhaar', 'A drowning man clutches a straw', 'A desperate person will try anything', 'A drowning man clutches at a straw', None),
            ('Marathi', 'धीर धरा फळ मिळेल', 'Dheer dhara phal milel', 'Be patient and you will get the fruit', 'Good things come to those who wait', 'Patience is a virtue', None),
            ('Marathi', 'खाण तशी माती', 'Khaan tashi maati', 'As the mine so the soil', 'The environment you come from shapes who you are', 'As the twig is bent so grows the tree', None),
            ('Marathi', 'विद्या हे खरे धन', 'Vidya he khare dhan', 'Knowledge is true wealth', 'Education and wisdom are the most valuable possessions', 'Knowledge is power', None),
            ('Marathi', 'अनुभव हा सर्वोत्तम शिक्षक', 'Anubhav ha sarvottam shikshak', 'Experience is the best teacher', 'Learning from real life is the most powerful education', 'Experience is the best teacher', None),
            ('Marathi', 'माणसाला माणूसच ओळखतो', 'Maansaala maanus olakhato', 'Only a person recognizes another person', 'Empathy comes from shared human experience', 'It takes one to know one', None),
            ('Marathi', 'मनात आणले की जमते', 'Manaat aanlele ki jamte', 'If you put your mind to it it works out', 'Determination and focus make things possible', 'Where there is a will there is a way', None),
            ('Marathi', 'शेजारची कोंबडी जड', 'Shejaarchi kombdi jad', 'The neighbour s hen seems heavier', 'People always think others have more than they do', 'The grass is greener on the other side', None),
            ('Marathi', 'लहान तोंडी मोठा घास', 'Lahaan tondi motha ghaas', 'A big morsel for a small mouth', 'Taking on more than you can handle', 'Biting off more than you can chew', None),
            ('Marathi', 'काळ हे सर्वोत्तम औषध आहे', 'Kaal he sarvottam aushadha aahe', 'Time is the best medicine', 'Time heals all wounds and sorrows', 'Time heals all wounds', None),
            ('Marathi', 'एकट्याने जाऊ नये', 'Ekatyaane jaau naye', 'One should not go alone', 'Some goals require companionship and teamwork', 'No man is an island', None),
            ('Marathi', 'दयेपेक्षा मोठा धर्म नाही', 'Dayepeksha motha dharm naahi', 'There is no religion greater than compassion', 'Kindness and empathy are the highest virtues', 'Kindness costs nothing', None),
            ('Marathi', 'छोट्या छोट्या पावलांनी मोठे बदल होतात', 'Chhottya chhottya paawalanni mothe badal hotat', 'Small steps bring big changes', 'Gradual consistent effort creates major transformation', 'Small steps lead to big changes', None),
            ('Marathi', 'वयाबरोबर शहाणपण येते', 'Vayaabarobar shahaanapan yete', 'Wisdom comes with age', 'Experience and years bring greater understanding', 'Wisdom comes with age', None),
            ('Marathi', 'शिकणे कधीच संपत नाही', 'Shikane kadhich sampat naahi', 'Learning never ends', 'There is always something new to learn at every age', 'Learning never ends', None),
            ('Marathi', 'जे मोडलेले नाही ते दुरुस्त करू नका', 'Je modalele naahi te durust karu nakaa', 'Do not fix what is not broken', 'Do not change something that is already working well', "If it ain't broke don't fix it", None),
            ('Marathi', 'घाई केल्याने काम बिघडते', 'Ghaaee kellyaane kaam bighadate', 'Hurrying ruins the work', 'Rushing leads to mistakes', 'Haste makes waste', None),
            ('Marathi', 'जो पेरतो तो कापतो', 'Jo perato to kaapato', 'Whoever sows also reaps', 'Your efforts determine your rewards', 'You reap what you sow', None),
            ('Marathi', 'एकत्र राहिलो तर जगू', 'Ekatra raahilo tar jagu', 'If we stay together we will live', 'Unity and cooperation are essential for survival', 'United we stand divided we fall', None),
            ('Marathi', 'गर्जना करणारा बरसत नाही', 'Garjana karanara barsat naahi', 'The one who thunders does not rain', 'Those who boast rarely deliver', 'Barking dogs seldom bite', None),
            ('Marathi', 'सत्य लपवता येत नाही', 'Satya lapawata yet naahi', 'Truth cannot be hidden', 'The truth always comes out eventually', 'Truth will out', None),
            ('Marathi', 'मोठ्याने बोलणे म्हणजे शहाणपण नाही', 'Mothyaane bolane mhanje shahaanapan naahi', 'Speaking loudly is not wisdom', 'Volume and confidence are not the same as intelligence', 'Empty vessels make the most noise', None),
            ('Marathi', 'नशीब स्वतः घडवावे लागते', 'Nashib swatah ghadawaawe lagate', 'One has to make their own fortune', 'Success comes from your own efforts not luck alone', 'God helps those who help themselves', None),
            ('Marathi', 'प्रत्येक कुत्र्याचा दिवस येतो', 'Pratyek kutryacha diwas yeto', 'Every dog has its day', 'Everyone gets their moment of success or recognition', 'Every dog has its day', None),
            ('Marathi', 'मित्र मिळवणे सोपे गमावणे सोपे', 'Mitra milavane sope gamawane sope', 'Easy to make friends easy to lose them', 'Relationships require care and effort to maintain', 'Easy come easy go', None),
            ('Marathi', 'उपकार केलेला विसरू नये', 'Upakaar kelela visaru naye', 'Do not forget the kindness done to you', 'Always remember and honour those who helped you', 'Gratitude is the sign of noble souls', None),
            ('Marathi', 'मेहनत हीच खरी पूजा', 'Mehnat hich khari pooja', 'Hard work is the truest form of worship', 'Diligence and dedication are the highest virtues', 'Hard work pays off', None),
            ('Marathi', 'लोभ हा सर्व दुःखांचे मूळ', 'Lobh ha sarv dukhaanche mool', 'Greed is the root of all suffering', 'Greed leads to downfall and sorrow', 'Greed is the root of all evil', None),
            ('Marathi', 'संगत तशी रंगत', 'Sangat tashi rangat', 'You take on the colour of your company', 'You become like the people you spend time with', 'You are known by the company you keep', None),
            ('Marathi', 'हार मानणे म्हणजे हरणे', 'Haar maanane mhanje harane', 'Accepting defeat means losing', 'You only truly lose when you stop trying', 'It is not over until it is over', None),
            ('Marathi', 'जगणे शिकवते', 'Jagane shikawate', 'Living teaches', 'Life itself is the greatest teacher', 'Experience is the best teacher', None),
            ('Marathi', 'काम केल्याशिवाय फळ नाही', 'Kaam kellyashivaay phal naahi', 'Without doing work there is no fruit', 'Results only come through action and effort', 'No pain no gain', None),
            ('Marathi', 'जे गेले ते गेले', 'Je gele te gele', 'What has gone has gone', 'Do not dwell on what cannot be changed', 'Let bygones be bygones', None),
            ('Marathi', 'ज्याचे काम त्यालाच साजे', 'Jyache kaam tyaalach saaje', 'Work suits only the one it belongs to', 'Every person has their own unique skills', 'Each to their own', None),
            ('Marathi', 'बोलण्यापेक्षा करणे श्रेयस्कर', 'Bolanyapeksha karane shreyas kar', 'Doing is better than talking', 'Actions are worth more than words', 'Actions speak louder than words', None),
            ('Marathi', 'नाते जपले तरच टिकते', 'Naate japale tarach tikate', 'A relationship survives only if it is nurtured', 'Relationships need care and effort to last', 'A friendship maintained is a friendship gained', None),
            ('Marathi', 'खरे बोलण्यास धाडस लागते', 'Khare bolanyaas dhadas lagate', 'Speaking the truth requires courage', 'Honesty demands bravery', 'Honesty is the best policy', None),
            ('Marathi', 'ज्ञान हे शस्त्रापेक्षा बलवान', 'Dnyan he shastraapeksha balawan', 'Knowledge is more powerful than a weapon', 'Education and wisdom overcome all obstacles', 'The pen is mightier than the sword', None),
            ('Marathi', 'आळशी माणसाला वेळ नसतो', 'Aalshi maansaala vel nasato', 'A lazy person never has time', 'Those who waste time always claim they have none', 'Idle hands find no work done', None),
            ('Marathi', 'प्रेम आंधळे असते', 'Prem aandhale asate', 'Love is blind', 'Love makes people overlook faults in those they care about', 'Love is blind', None),
            ('Marathi', 'चांगल्या माणसाचा सगळीकडे मान', 'Chhanglya maansacha sagalikade maan', 'A good person is respected everywhere', 'Virtue and good character earn respect universally', 'Goodness is its own reward', None),
            ('Marathi', 'नदीत राहून माशाशी वैर नको', 'Nadit rahun mashaashi vair nako', 'Living in the river do not make enemies with the fish', 'Do not fight with those who are powerful in their own domain', 'Do not bite the hand that feeds you', None),
            ('Marathi', 'दिव्याखाली अंधार', 'Divyakhali andhaar', 'Darkness under the lamp', 'Those closest to the source are often least aware of it', 'The cobbler s children have no shoes', None),
            ('Marathi', 'सांगितले तेव्हा ऐकले नाही', 'Saangitle tevha aikale naahi', 'Did not listen when told', 'Ignoring good advice leads to regret later', 'You were warned', None),
        ]

        cursor.executemany('''
            INSERT INTO proverbs (language, script, romanised, literal_translation, real_meaning, english_equivalent, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', proverbs)

        # Seed cross-language equivalents
        equivalents = [
            ('ટીપે ટીપે સરોવર ભરાય', 'Gujarati', 'Hindi', 'बूंद बूंद से सागर भरता है', 'Bund bund se saagar bharta hai'),
            ('ટીપે ટીપે સરોવર ભરાય', 'Gujarati', 'Marathi', 'थेंबे थेंबे तळे साचे', 'Theme theme tale saache'),
            ('बूंद बूंद से सागर भरता है', 'Hindi', 'Gujarati', 'ટીપે ટીપે સરોવર ભરાય', 'Tipe tipe sarovar bharay'),
            ('बूंद बूंद से सागर भरता है', 'Hindi', 'Marathi', 'थेंबे थेंबे तळे साचे', 'Theme theme tale saache'),
            ('थेंबे थेंबे तळे साचे', 'Marathi', 'Gujarati', 'ટીપે ટીપે સરોવર ભરાય', 'Tipe tipe sarovar bharay'),
            ('थेंबे थेंबे तळे साचे', 'Marathi', 'Hindi', 'बूंद बूंद से सागर भरता है', 'Bund bund se saagar bharta hai'),
            ('દૂધનો દાઝેલો છાશ પણ ફૂંકી ફૂંકીને પીએ', 'Gujarati', 'Hindi', 'दूध का जला छाछ भी फूंक फूंक कर पीता है', 'Dudh ka jala chaach bhi funky funk kar peeta hai'),
            ('दूध का जला छाछ भी फूंक फूंक कर पीता है', 'Hindi', 'Gujarati', 'દૂધનો દાઝેલો છાશ પણ ફૂંકી ફૂંકીને પીએ', 'Dudh no daazelo chaash pan funki funkine piye'),
            ('દૂરથી ડુંગર રળિયામણા', 'Gujarati', 'Marathi', 'दुरून डोंगर साजरे', 'Duroon dongar saajare'),
            ('દૂરથી ડુંગર રળિયામણા', 'Gujarati', 'Hindi', 'दूर के ढोल सुहावने', 'Door ke dhol suhavne'),
            ('दुरून डोंगर साजरे', 'Marathi', 'Gujarati', 'દૂરથી ડુંગર રળિયામણા', 'Durathi dungar radiyamna'),
            ('दुरून डोंगर साजरे', 'Marathi', 'Hindi', 'दूर के ढोल सुहावने', 'Door ke dhol suhavne'),
            ('दूर के ढोल सुहावने', 'Hindi', 'Gujarati', 'દૂરથી ડુંગર રળિયામણા', 'Durathi dungar radiyamna'),
            ('दूर के ढोल सुहावने', 'Hindi', 'Marathi', 'दुरून डोंगर साजरे', 'Duroon dongar saajare'),
            ('નાચ ન જાણે આંગણ વાંકુ', 'Gujarati', 'Hindi', 'नाच न जाने आंगन टेढ़ा', 'Naach na jaane aangan tedha'),
            ('નાચ ન જાણે આંગણ વાંકુ', 'Gujarati', 'Marathi', 'नाचता येईना अंगण वाकडे', 'Nachata yeina angan vakade'),
            ('नाच न जाने आंगन टेढ़ा', 'Hindi', 'Gujarati', 'નાચ ન જાણે આંગણ વાંકુ', 'Naach na jaane aangan vaanku'),
            ('नाच न जाने आंगन टेढ़ा', 'Hindi', 'Marathi', 'नाचता येईना अंगण वाकडे', 'Nachata yeina angan vakade'),
            ('नाचता येईना अंगण वाकडे', 'Marathi', 'Gujarati', 'નાચ ન જાણે આંગણ વાંકુ', 'Naach na jaane aangan vaanku'),
            ('नाचता येईना अंगण वाकडे', 'Marathi', 'Hindi', 'नाच न जाने आंगन टेढ़ा', 'Naach na jaane aangan tedha'),
            ('જ્યાં ઇચ્છા ત્યાં માર્ગ', 'Gujarati', 'Hindi', 'जहाँ चाह वहाँ राह', 'Jahan chaah wahaan raah'),
            ('જ્યાં ઇચ્છા ત્યાં માર્ગ', 'Gujarati', 'Marathi', 'जिथे इच्छा तिथे मार्ग', 'Jithe ichchha tithe maarg'),
            ('जहाँ चाह वहाँ राह', 'Hindi', 'Gujarati', 'જ્યાં ઇચ્છા ત્યાં માર્ગ', 'Jyaan ichchha tyaan maarg'),
            ('जहाँ चाह वहाँ राह', 'Hindi', 'Marathi', 'जिथे इच्छा तिथे मार्ग', 'Jithe ichchha tithe maarg'),
            ('जिथे इच्छा तिथे मार्ग', 'Marathi', 'Gujarati', 'જ્યાં ઇચ્છા ત્યાં માર્ગ', 'Jyaan ichchha tyaan maarg'),
            ('जिथे इच्छा तिथे मार्ग', 'Marathi', 'Hindi', 'जहाँ चाह वहाँ राह', 'Jahan chaah wahaan raah'),
            ('જેવું વાવો તેવું લણો', 'Gujarati', 'Hindi', 'जैसी करनी वैसी भरनी', 'Jaisi karni waisi bharni'),
            ('જેવું વાવો તેવું લણો', 'Gujarati', 'Marathi', 'जशी करणी तशी भरणी', 'Jashi karani tashi bharani'),
            ('जैसी करनी वैसी भरनी', 'Hindi', 'Gujarati', 'જેવું વાવો તેવું લણો', 'Jevu vaavo tevu lano'),
            ('जैसी करनी वैसी भरनी', 'Hindi', 'Marathi', 'जशी करणी तशी भरणी', 'Jashi karani tashi bharani'),
            ('जशी करणी तशी भरणी', 'Marathi', 'Gujarati', 'જેવું વાવો તેવું લણો', 'Jevu vaavo tevu lano'),
            ('जशी करणी तशी भरणी', 'Marathi', 'Hindi', 'जैसी करनी वैसी भरनी', 'Jaisi karni waisi bharni'),
            ('अति सर्वत्र वर्जयेत', 'Hindi', 'Gujarati', 'અતિ સર્વત્ર વર્જયેત', 'Ati sarvatra varjayet'),
            ('अति सर्वत्र वर्जयेत', 'Hindi', 'Marathi', 'अति तिथे माती', 'Ati tithe maati'),
            ('અતિ સર્વત્ર વર્જયેત', 'Gujarati', 'Hindi', 'अति सर्वत्र वर्जयेत', 'Ati sarvatra varjayet'),
            ('અતિ સર્વત્ર વર્જયેત', 'Gujarati', 'Marathi', 'अति तिथे माती', 'Ati tithe maati'),
            ('अति तिथे माती', 'Marathi', 'Gujarati', 'અતિ સર્વત્ર વર્જયેત', 'Ati sarvatra varjayet'),
            ('अति तिथे माती', 'Marathi', 'Hindi', 'अति सर्वत्र वर्जयेत', 'Ati sarvatra varjayet'),
            ('एक हाथ से ताली नहीं बजती', 'Hindi', 'Gujarati', 'એક હાથે તાળી ન પડે', 'Ek haathe taali na pade'),
            ('एक हाथ से ताली नहीं बजती', 'Hindi', 'Marathi', 'एका हाताने टाळी वाजत नाही', 'Eka haatane taali vaajat naahi'),
            ('એક હાથે તાળી ન પડે', 'Gujarati', 'Hindi', 'एक हाथ से ताली नहीं बजती', 'Ek haath se taali nahi bajti'),
            ('એક હાથે તાળી ન પડે', 'Gujarati', 'Marathi', 'एका हाताने टाळी वाजत नाही', 'Eka haatane taali vaajat naahi'),
            ('एका हाताने टाळी वाजत नाही', 'Marathi', 'Gujarati', 'એક હાથે તાળી ન પડે', 'Ek haathe taali na pade'),
            ('एका हाताने टाळी वाजत नाही', 'Marathi', 'Hindi', 'एक हाथ से ताली नहीं बजती', 'Ek haath se taali nahi bajti'),
            ('घर का भेदी लंका ढाए', 'Hindi', 'Marathi', 'घरचा भेदी लंका जाळी', 'Gharcha bhedi lanka jaali'),
            ('घरचा भेदी लंका जाळी', 'Marathi', 'Hindi', 'घर का भेदी लंका ढाए', 'Ghar ka bhedi lanka dhaye'),
        ]

        for src_script, src_lang, tgt_lang, tgt_script, tgt_roman in equivalents:
            cursor.execute("SELECT id FROM proverbs WHERE script = ? AND language = ?", (src_script, src_lang))
            row = cursor.fetchone()
            if row:
                cursor.execute('''
                    INSERT INTO proverb_equivalents (proverb_id, target_language, equivalent_script, equivalent_romanised)
                    VALUES (?, ?, ?, ?)
                ''', (row['id'], tgt_lang, tgt_script, tgt_roman))

    conn.commit()
    conn.close()


def _normalise(text):
    """Normalise Indian language text for fuzzy matching.
    Handles common Unicode variants:
    - chandrabindu (ँ) vs anusvara (ं) in Hindi/Marathi
    - visarga and other diacritic variants
    - strips extra whitespace
    """
    import unicodedata
    # Normalise to NFC form first
    text = unicodedata.normalize('NFC', text.strip())
    # Map chandrabindu to anusvara for Hindi/Marathi matching
    text = text.replace('\u0901', '\u0902')  # ँ → ं
    # Collapse multiple spaces
    text = ' '.join(text.split())
    return text.lower()


def find_proverb(text, source_lang, target_lang=None):
    conn = get_db()
    cursor = conn.cursor()

    # First try exact match
    cursor.execute('''
        SELECT * FROM proverbs
        WHERE language = ?
        AND (script = ? OR LOWER(romanised) = LOWER(?) OR LOWER(script) = LOWER(?))
    ''', (source_lang, text.strip(), text.strip(), text.strip()))
    result = cursor.fetchone()

    # If exact match fails, try normalised fuzzy match
    if not result:
        normalised_input = _normalise(text)
        cursor.execute('SELECT * FROM proverbs WHERE language = ?', (source_lang,))
        all_proverbs = cursor.fetchall()
        for row in all_proverbs:
            if _normalise(row['script']) == normalised_input:
                result = row
                break
            if row['romanised'] and _normalise(row['romanised']) == normalised_input:
                result = row
                break

    if not result:
        conn.close()
        return None

    proverb = dict(result)

    if target_lang:
        cursor.execute('''
            SELECT * FROM proverb_equivalents
            WHERE proverb_id = ? AND target_language = ?
        ''', (proverb['id'], target_lang))
        equivalent = cursor.fetchone()
        proverb['target_equivalent'] = dict(equivalent) if equivalent else None

    conn.close()
    return proverb


def log_feedback(source_lang, target_lang, input_text, translation, rating, comment=''):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (source_lang, target_lang, input_text, translation, rating, comment)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (source_lang, target_lang, input_text or '', translation or '', rating, comment or ''))
    conn.commit()
    conn.close()


def log_usage(source_lang, target_lang, input_length, success=True):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usage_stats (source_lang, target_lang, input_length, success)
        VALUES (?, ?, ?, ?)
    ''', (source_lang, target_lang, input_length, success))
    conn.commit()
    conn.close()


def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as total FROM usage_stats WHERE success = 1')
    total = cursor.fetchone()['total']

    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) as total FROM usage_stats WHERE DATE(created_at) = ? AND success = 1", (today,))
    today_count = cursor.fetchone()['total']

    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) as total FROM usage_stats WHERE DATE(created_at) >= ? AND success = 1", (week_ago,))
    week_count = cursor.fetchone()['total']

    cursor.execute('''
        SELECT source_lang || ' → ' || target_lang as pair, COUNT(*) as count
        FROM usage_stats WHERE success = 1
        GROUP BY source_lang, target_lang
        ORDER BY count DESC LIMIT 8
    ''')
    top_pairs = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT COUNT(*) as total FROM feedback WHERE rating = 'good'")
    good = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM feedback WHERE rating = 'bad'")
    bad = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) as total FROM proverbs')
    proverb_count = cursor.fetchone()['total']

    conn.close()
    return {
        'total': total,
        'today': today_count,
        'this_week': week_count,
        'top_pairs': top_pairs,
        'thumbs_up': good,
        'thumbs_down': bad,
        'proverb_count': proverb_count
    }


def get_recent_feedback():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM feedback
        ORDER BY created_at DESC LIMIT 15
    ''')
    results = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return results


def get_recent_translations():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM usage_stats
        ORDER BY created_at DESC LIMIT 15
    ''')
    results = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return results
