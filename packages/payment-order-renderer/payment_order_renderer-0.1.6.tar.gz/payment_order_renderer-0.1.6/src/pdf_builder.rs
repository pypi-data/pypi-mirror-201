use printpdf::*;
use std::fs::File;
use std::io::Cursor;

use crate::PaymentOrder; 


const LONG_HRZ_LINE_COORD1: (Mm, Mm) = (Mm(19.6), Mm(248.0));
const LONG_HRZ_LINE_COORD2: (Mm, Mm) = (Mm(19.6), Mm(203.0));
const LONG_HRZ_LINE_COORD3: (Mm, Mm) = (Mm(19.6), Mm(152.0));
const LONG_HRZ_LINE_COORD4: (Mm, Mm) = (Mm(19.6), Mm(147.0));
const LONG_HRZ_LINE_COORD5: (Mm, Mm) = (Mm(19.6), Mm(123.0));

const MEDIUM_LONG_HRZ_LINE_COORD1: (Mm, Mm) = (Mm(19.6), Mm(217.8));
const MEDIUM_LONG_HRZ_LINE_COORD2: (Mm, Mm) = (Mm(19.6), Mm(187.8));

const SHORT_HRZ_LINE_COORD1: (Mm, Mm) = (Mm(79.5), Mm(107.0));
const SHORT_HRZ_LINE_COORD2: (Mm, Mm) = (Mm(79.5), Mm(92.0));

const BIK_HRZ_LINE_COORD1: (Mm, Mm) = (Mm(119.6), Mm(212.9));
const BIK_HRZ_LINE_COORD2: (Mm, Mm) = (Mm(119.6), Mm(197.9));
const TYPEH_RZ_LINE_COORD:(Mm, Mm) = (Mm(119.6), Mm(168.2));
const PURPOSE_HRZ_LINE_COORD: (Mm, Mm) = (Mm(119.6), Mm(163.2));
const MIDDLE_SHORT_RZ_LINE_COORD1:(Mm, Mm) = (Mm(119.6), Mm(152.0));
const MIDDLE_SHORT_RZ_LINE_COORD2: (Mm, Mm) = (Mm(154.4), Mm(168.2));
const MIDDLE_SHORT_RZ_LINE_COORD3: (Mm, Mm) = (Mm(154.4), Mm(163.2));

const DATE_HRZ_LINE_COORD1: (Mm, Mm) = (Mm(19.6), Mm(282.1));
const DATE_HRZ_LINE_COORD2: (Mm, Mm) = (Mm(64.6), Mm(282.1));
const DATE_HRZ_LINE_COORD3: (Mm, Mm) = (Mm(83.0), Mm(266.8));
const TYPE_HRZ_LINE_COORD: (Mm, Mm) = (Mm(128.0), Mm(266.8));

const MEDIUM_HRZ_LINE_COORD1: (Mm, Mm) = (Mm(19.6), Mm(243.0));
const MEDIUM_HRZ_LINE_COORD2: (Mm, Mm) = (Mm(119.6), Mm(232.8));
const MEDIUM_HRZ_LINE_COORD3: (Mm, Mm) = (Mm(119.6), Mm(173.0));
const MEDIUM_HRZ_LINE_COORD4: (Mm, Mm) = (Mm(19.6), Mm(183.0));

const SHORT_VRT_LINE_COORD1: (Mm, Mm) = (Mm(39.6), Mm(248.0));
const SHORT_VRT_LINE_COORD2: (Mm, Mm) = (Mm(154.4), Mm(152.0));
const SHORT_VRT_LINE_COORD3: (Mm, Mm) = (Mm(174.5), Mm(152.0));

const LONG_VRT_LINE_COORD1: (Mm, Mm) = (Mm(119.6), Mm(152.0));
const LONG_VRT_LINE_COORD2: (Mm, Mm) = (Mm(134.6), Mm(152.0));

const MICRO_SHORT_VRT_LINE_COORD1: (Mm, Mm) = (Mm(69.6), Mm(243.0));
const MICRO_SHORT_VRT_LINE_COORD2: (Mm, Mm) = (Mm(69.6), Mm(183.1));
const MICRO_SHORT_VRT_LINE_COORD3: (Mm, Mm) = (Mm(64.3), Mm(147.0));
const MICRO_SHORT_VRT_LINE_COORD4: (Mm, Mm) = (Mm(94.7), Mm(147.0));
const MICRO_SHORT_VRT_LINE_COORD5: (Mm, Mm) = (Mm(104.6), Mm(147.0));
const MICRO_SHORT_VRT_LINE_COORD6: (Mm, Mm) = (Mm(129.8), Mm(147.0));
const MICRO_SHORT_VRT_LINE_COORD7: (Mm, Mm) = (Mm(164.6), Mm(147.0));
const MICRO_SHORT_VRT_LINE_COORD8: (Mm, Mm) = (Mm(189.7), Mm(147.0));


//Дефолтный текст
const INCOME_COORD: (Mm, Mm) = (Mm(22.4), Mm(279.3));
const OUTCOME_COORD: (Mm, Mm) = (Mm(67.3), Mm(279.3));

const DATE_COORD: (Mm, Mm) = (Mm(97.0), Mm(264.0));
const DIGITAL_COORD: (Mm, Mm) = (Mm(137.2), Mm(267.8));
const ORDER_TYPE_COORD: (Mm, Mm) = (Mm(136.4), Mm(264.0));
const PAYMENT_ORDER_COORD: (Mm, Mm) = (Mm(19.8), Mm(267.8));//bold

const OKTMO_NUMBER_COORD: (Mm, Mm) = (Mm(186.4), Mm(285.3));

const LITERAL_SUM_COORD: (Mm, Mm) = (Mm(19.8), Mm(259.9)); // width Mm(19)

const INN1_COORD: (Mm, Mm) = (Mm(19.8), Mm(244.7));
const KPP1_COORD: (Mm, Mm) = (Mm(70.4), Mm(244.7));
const SUM_COORD: (Mm, Mm) = (Mm(120.1), Mm(244.7));

const ACCOUNT_NUMBER1_COORD: (Mm, Mm) = (Mm(120.1), Mm(229.2));

const PAYER_COORD: (Mm, Mm) = (Mm(19.8), Mm(219.1));

const BIK1_COORD: (Mm, Mm) = (Mm(120.1), Mm(214.2));
const ACCOUNT_NUMBER2_COORD: (Mm, Mm) = (Mm(120.1), Mm(209.6));

const PAYER_BANK_COORD: (Mm, Mm) = (Mm(19.8), Mm(204.3));

const BIK2_COORD: (Mm, Mm) = (Mm(120.1), Mm(199.8));
const ACCOUNT_NUMBER3_COORD: (Mm, Mm) = (Mm(120.1), Mm(194.9));

const PAYEE_BANK_COORD: (Mm, Mm) = (Mm(19.8), Mm(189.1));

const INN2_COORD: (Mm, Mm) = (Mm(19.8), Mm(184.8));
const KPP2_COORD: (Mm, Mm) = (Mm(70.4), Mm(184.8));
const ACCOUNT_NUMBER4_COORD: (Mm, Mm) = (Mm(120.1), Mm(184.8));

const PAYMENT_TYPE_COORD: (Mm, Mm) = (Mm(120.1), Mm(169.8));
const PAYMENT_TERM_COORD: (Mm, Mm) = (Mm(154.9), Mm(169.8));

const PAYMENT_PURPOSE_COORD: (Mm, Mm) = (Mm(120.1), Mm(164.5));
const PAYMENT_QUE_COORD: (Mm, Mm) = (Mm(154.9), Mm(164.8));

const PAYMENT_CODE_COORD: (Mm, Mm) = (Mm(120.1), Mm(159.8));
const PAYMENT_RESERVE_COORD: (Mm, Mm) = (Mm(154.9), Mm(159.8));

const PAYEE_COORD: (Mm, Mm) = (Mm(19.8), Mm(153.0));

const PAYMENT_PURPOSE_FULL_COORD: (Mm, Mm) = (Mm(20.1), Mm(124.3));

const SIGN_COORD: (Mm, Mm) = (Mm(103.4), Mm(119.5));
const BANK_SIGNS_COORD: (Mm, Mm) = (Mm(159.0), Mm(119.5));

const PAID_COORD: (Mm, Mm) = (Mm(162.8), Mm(111.3));//blue

const STAMP_COORD: (Mm, Mm) = (Mm(46.5), Mm(101.2));


//Текст с данными
const DATA_INCOME_COORD: (Mm, Mm) = (Mm(29.4), Mm(282.8));
const DATA_OUTCOME_COORD: (Mm, Mm) = (Mm(74.4), Mm(282.8));
const DATA_PAYMENT_ORDER_COORD: (Mm, Mm) = (Mm(66.5), Mm(267.8));//bold
const DATA_DATE_COORD: (Mm, Mm) = (Mm(92.7), Mm(267.7));
const DATA_LITERAL_SUM_COORD: (Mm, Mm) = (Mm(41.4), Mm(259.9)); // width Mm(158.5)

const DATA_INN1_COORD: (Mm, Mm) = (Mm(28.7), Mm(244.7));
const DATA_KPP1_COORD: (Mm, Mm) = (Mm(78.7), Mm(244.7));
const DATA_SUM_COORD: (Mm, Mm) = (Mm(135.1), Mm(244.7));

const DATA_PAYER_COORD: (Mm, Mm) = (Mm(19.8), Mm(239.6)); //99.5

const DATA_ACCOUNT_NUMBER1_COORD: (Mm, Mm) = (Mm(135.1), Mm(229.2));

const DATA_PAYER_BANK_COORD: (Mm, Mm) = (Mm(19.8), Mm(214.2));//99.5
const DATA_BIK1_COORD: (Mm, Mm) = (Mm(135.1), Mm(214.2));

const DATA_ACCOUNT_NUMBER2_COORD: (Mm, Mm) = (Mm(135.1), Mm(209.6));

const DATA_PAYEE_BANK_COORD: (Mm, Mm) = (Mm(19.8), Mm(199.5));
const DATA_BIK2_COORD: (Mm, Mm) = (Mm(135.1), Mm(199.5));
const DATA_ACCOUNT_NUMBER3_COORD: (Mm, Mm) = (Mm(135.1), Mm(194.6));

const DATA_INN2_COORD: (Mm, Mm) = (Mm(28.7), Mm(184.8));
const DATA_KPP2_COORD: (Mm, Mm) = (Mm(78.7), Mm(184.8));
const DATA_ACCOUNT_NUMBER4_COORD: (Mm, Mm) = (Mm(135.1), Mm(184.8));

const DATA_PAYEE_COORD: (Mm, Mm) = (Mm(19.8), Mm(179.9));

const DATA_PAYMENT_CODE_COORD: (Mm, Mm) = (Mm(135.1), Mm(169.2));

const DATA_PAYMENT_QUE_COORD: (Mm, Mm) = (Mm(175.0), Mm(164.8));
const DATA_FULL_PURPOSE_COORD: (Mm, Mm) = (Mm(19.8), Mm(143.9)); //180.1

const DATA_PAID: (Mm, Mm) = (Mm(163.6), Mm(107.8));

const HEAD_FULL_NAME_COORD: (Mm, Mm) = (Mm(167.1), Mm(35.9));


//Необязательные параметры
const DATA_PURPOSE_CODE: (Mm, Mm) = (Mm(135.1), Mm(164.8));
const DATA_UIN_CODE: (Mm, Mm) = (Mm(135.1), Mm(159.8));
const DATA_STATUS: (Mm, Mm) = (Mm(194.5), Mm(270.1));
const DATA_CBC: (Mm, Mm) = (Mm(19.8), Mm(148.7));
const DATA_OKATO: (Mm, Mm) = (Mm(65.0), Mm(148.7));
const DATA_REASON: (Mm, Mm) = (Mm(95.2), Mm(148.7));
const DATA_PERIOD: (Mm, Mm) = (Mm(105.2), Mm(148.7));
const DATA_REASON_NUMBER: (Mm, Mm) = (Mm(130.3), Mm(148.7));
const DATA_REASON_DATE: (Mm, Mm) = (Mm(165.4), Mm(148.7));
const DATA_FIELD_110: (Mm, Mm) = (Mm(190.2), Mm(148.7));


//Координаты прямоугольных форм
const OKTMO_COORDS: (Mm, Mm, Mm, Mm) = (Mm(185.2), Mm(290.4), Mm(199.9), Mm(283.1));
const PRIORITY_COORDS: (Mm, Mm, Mm, Mm) = (Mm(192.8), Mm(274.6), Mm(199.9), Mm(267.6));
const BANK_SIGNS_COORDS: (Mm, Mm, Mm, Mm) = (Mm(151.9), Mm(114.1), Mm(187.2), Mm(106.8));


const ARIAL: &[u8] = include_bytes!("../src/fonts/Arial.ttf");
const ARIAL_BOLD: &[u8] = include_bytes!("../src/fonts/Arial Bold.ttf");


fn add_rectangle(layer: &PdfLayerReference, coords: (Mm, Mm, Mm, Mm), color: &Color) {
    /* Добавить прямоугольник на документ */

    let points: Vec<(printpdf::Point, bool)> = vec![
        (Point::new(coords.0, coords.1), false),
        (Point::new(coords.0, coords.3), false),
        (Point::new(coords.2, coords.3), false),
        (Point::new(coords.2, coords.1), false),
        (Point::new(coords.0, coords.1), false),
    ];
    
    let rect = Line {
        points,
        is_closed: false,
        has_fill: false,
        has_stroke: true,
        is_clipping_path: false,
    };

    layer.set_outline_color(color.clone());
    layer.set_outline_thickness(1.0);

    layer.add_shape(rect);
}


fn add_line(layer: &PdfLayerReference, coords: (Mm, Mm), length: Mm, color: &Color, orientation: &str) {
    /* Добавить линию на документ */

    let points = match orientation {
        "horizontal" => vec![
            (Point::new(coords.0, coords.1), false),
            (Point::new(coords.0 + length, coords.1), false),
        ],
        "vertical" => vec![
            (Point::new(coords.0 , coords.1 + length), false),
            (Point::new(coords.0, coords.1), false),
        ],
        _ => panic!("Invalid orientation"),
    };

    let line = Line {
        points,
        is_closed: false,
        has_fill: false,
        has_stroke: true,
        is_clipping_path: false,
    };

    layer.set_outline_color(color.clone());
    layer.set_outline_thickness(1.0);

    layer.add_shape(line);
}


fn remove_alpha_channel_from_image_x_object(image_x_object: ImageXObject) -> ImageXObject {
    /* Костыль для добавления файлов формата png */
    if !matches!(image_x_object.color_space, ColorSpace::Rgba) {
        return image_x_object;
    };
    let ImageXObject {
        color_space,
        image_data,
        ..
    } = image_x_object;

    let new_image_data = image_data
        .chunks(4)
        .map(|rgba| {
            let [red, green, blue, alpha]: [u8; 4] = rgba.try_into().ok().unwrap();
            let alpha = alpha as f64 / 255.0;
            let new_red = ((1.0 - alpha) * 255.0 + alpha * red as f64) as u8;
            let new_green = ((1.0 - alpha) * 255.0 + alpha * green as f64) as u8;
            let new_blue = ((1.0 - alpha) * 255.0 + alpha * blue as f64) as u8;
            return [new_red, new_green, new_blue];
        })
        .collect::<Vec<[u8; 3]>>()
        .concat();

    let new_color_space = match color_space {
        ColorSpace::Rgba => ColorSpace::Rgb,
        ColorSpace::GreyscaleAlpha => ColorSpace::Greyscale,
        other_type => other_type,
    };

    ImageXObject {
        color_space: new_color_space,
        image_data: new_image_data,
        ..image_x_object
    }
}


fn wrap_text_by_words(text: &str, font_size: f64, max_width: f64) -> Vec<String> {
    /* Перенос по словам */
    let words: Vec<&str> = text.split_whitespace().collect();
    let mut lines = Vec::new();
    let mut line = String::new();
    let mut line_width = 0.0;
    let wide_coefficient = 1.5; //Небольшая поправка по ширине текста
    
    for word in words {
        let word_width = word.chars().count() as f64 * font_size / 2.0;
        if line_width + word_width > max_width * wide_coefficient  { 
            lines.push(line.trim().to_string());
            line.clear();
            line_width = 0.0;
        }
        line.push_str(word);
        line.push(' ');
        line_width += word_width;
    }
    lines.push(line.trim().to_string());
    
    lines
}


fn write_text_to_pdf(
    layer: &PdfLayerReference,
    coords: (Mm, Mm),
    text: &str,
    size: f64,
    font: &IndirectFontRef,
    color: &Color,
    field_width: Option<Mm>,
) {
    let mut text_lines = vec![text.to_string()];
    if let Some(max_width) = field_width {
        text_lines = wrap_text_by_words(text, size, max_width.0);
    }

    layer.set_fill_color(color.clone());

    for (index, line) in text_lines.iter().enumerate() {
        let y_coord = if index != 0 {
            coords.1 - Mm(3 as f64)
        } else {
            coords.1
        };
        layer.use_text(line, size, coords.0, y_coord, &font);
    }
}


pub fn create_payment_report(payment_order: &PaymentOrder, path: &str) -> Result<Vec<u8>, PdfError> {

    let black = Color::Rgb(Rgb::new(0.0, 0.0, 0.0, None));
    let blue = Color::Rgb(Rgb::new(0.0, 0.0, 255.0, None));

    let black_ref = &black;
    let blue_ref = &blue;

    let lines: [((Mm, Mm), Mm, &Color, &'static str ); 37] = [
        (LONG_HRZ_LINE_COORD1, Mm(180.0), black_ref, "horizontal"),
        (LONG_HRZ_LINE_COORD2, Mm(180.0), black_ref, "horizontal"),
        (LONG_HRZ_LINE_COORD3, Mm(180.0), black_ref, "horizontal"),
        (LONG_HRZ_LINE_COORD4, Mm(180.0), black_ref, "horizontal"),
        (LONG_HRZ_LINE_COORD5, Mm(180.0), black_ref, "horizontal"),
        (MEDIUM_HRZ_LINE_COORD1, Mm(100.0), black_ref, "horizontal"),
        (MEDIUM_HRZ_LINE_COORD2, Mm(80.3), black_ref, "horizontal"),
        (MEDIUM_HRZ_LINE_COORD3, Mm(80.3), black_ref, "horizontal"),
        (MEDIUM_HRZ_LINE_COORD4, Mm(100.0), black_ref, "horizontal"),
        (MEDIUM_LONG_HRZ_LINE_COORD1, Mm(115.0), black_ref, "horizontal"),
        (MEDIUM_LONG_HRZ_LINE_COORD2, Mm(115.0), black_ref, "horizontal"),
        (SHORT_HRZ_LINE_COORD1, Mm(60.0), black_ref, "horizontal"),
        (SHORT_HRZ_LINE_COORD2, Mm(60.0), black_ref, "horizontal"),
        (DATE_HRZ_LINE_COORD1, Mm(35.0), black_ref, "horizontal"),
        (DATE_HRZ_LINE_COORD2, Mm(35.0), black_ref, "horizontal"),
        (DATE_HRZ_LINE_COORD3, Mm(35.0), black_ref, "horizontal"),
        (TYPE_HRZ_LINE_COORD, Mm(35.0), black_ref, "horizontal"),
        (BIK_HRZ_LINE_COORD1, Mm(15.0), black_ref, "horizontal"),
        (BIK_HRZ_LINE_COORD2, Mm(15.0), black_ref, "horizontal"),
        (TYPEH_RZ_LINE_COORD, Mm(15.0), black_ref, "horizontal"),
        (PURPOSE_HRZ_LINE_COORD, Mm(15.0), black_ref, "horizontal"),
        (MIDDLE_SHORT_RZ_LINE_COORD1, Mm(15.0), black_ref, "horizontal"),
        (MIDDLE_SHORT_RZ_LINE_COORD2, Mm(20.3), black_ref, "horizontal"),
        (MIDDLE_SHORT_RZ_LINE_COORD3, Mm(20.3), black_ref, "horizontal"),
        (SHORT_VRT_LINE_COORD1, Mm(15.3), black_ref, "vertical"),
        (SHORT_VRT_LINE_COORD2, Mm(21.1), black_ref, "vertical"),
        (SHORT_VRT_LINE_COORD3, Mm(21.1), black_ref, "vertical"),
        (LONG_VRT_LINE_COORD1, Mm(96.0), black_ref, "vertical"),
        (LONG_VRT_LINE_COORD2, Mm(96.0), black_ref, "vertical"),
        (MICRO_SHORT_VRT_LINE_COORD1, Mm(5.0), black_ref, "vertical"),
        (MICRO_SHORT_VRT_LINE_COORD2, Mm(5.0), black_ref, "vertical"),
        (MICRO_SHORT_VRT_LINE_COORD3, Mm(5.0), black_ref, "vertical"),
        (MICRO_SHORT_VRT_LINE_COORD4, Mm(5.0), black_ref, "vertical"),
        (MICRO_SHORT_VRT_LINE_COORD5, Mm(5.0), black_ref, "vertical"),
        (MICRO_SHORT_VRT_LINE_COORD6, Mm(5.0), black_ref, "vertical"),
        (MICRO_SHORT_VRT_LINE_COORD7, Mm(5.0), black_ref, "vertical"),
        (MICRO_SHORT_VRT_LINE_COORD8, Mm(5.0), black_ref, "vertical"),
        ];

    let rectangles: [((Mm, Mm, Mm, Mm), &Color); 3] = [
        (OKTMO_COORDS, black_ref),
        (PRIORITY_COORDS, black_ref),
        (BANK_SIGNS_COORDS, blue_ref),
    ];
    
    let (mut doc, page1, layer1) = PdfDocument::new(
        "payment_order",
        Mm(210.0),
        Mm(297.3),
        "Layer 1",
    );

    let current_layer = doc.get_page(page1).get_layer(layer1);

    let mut image_file = File::open(path).unwrap();
    let mut image = Image::try_from(image_crate::codecs::png::PngDecoder::new(&mut image_file).unwrap()).unwrap();

    image.image = remove_alpha_channel_from_image_x_object(image.image);

    // Размещаем печать по верхнему левому углу
    let x = Mm(120.0);
    let y = Mm(28.6);
    let mut image_transform = ImageTransform::default();

    image_transform.translate_x = Some(x);
    image_transform.translate_y = Some(y);

    image.add_to_layer(
        current_layer.clone(),
        image_transform,
    );

    let arial = doc.add_external_font(Cursor::new(ARIAL)).unwrap();
    let arial_bold = doc.add_external_font(Cursor::new(ARIAL_BOLD)).unwrap();

    let default_texts: [((Mm, Mm), &str, f64, &IndirectFontRef, &Color,  Option<Mm>); 34] = [ 
        (INCOME_COORD, "Поступ. в банк плат.", 9.0, &arial, black_ref, None),
        (OUTCOME_COORD, "Списано со сч. плат.", 9.0, &arial, black_ref, None),
        (DATE_COORD, "Дата", 9.0, &arial, black_ref, None),
        (DIGITAL_COORD, "Электронно", 9.0, &arial, black_ref, None),
        (ORDER_TYPE_COORD, "Вид платежа", 9.0, &arial, black_ref, None),
        (PAYMENT_ORDER_COORD, "ПЛАТЕЖНОЕ ПОРУЧЕНИЕ №", 9.0, &arial_bold, black_ref, None),
        (OKTMO_NUMBER_COORD, "0401060", 9.0, &arial, black_ref, None),
        (LITERAL_SUM_COORD, "Cумма прописью", 9.0, &arial, black_ref,Some(Mm(20.0))),
        (INN1_COORD, "ИНН", 9.0, &arial, black_ref, None),
        (KPP1_COORD, "КПП", 9.0, &arial, black_ref, None),
        (SUM_COORD, "Cумма", 9.0, &arial, black_ref, None),
        (ACCOUNT_NUMBER1_COORD, "Сч. №", 9.0, &arial, black_ref, None),
        (PAYER_COORD, "Плательщик", 9.0, &arial, black_ref, None),
        (BIK1_COORD, "БИК", 9.0, &arial, black_ref, None),
        (ACCOUNT_NUMBER2_COORD, "Сч. №", 9.0, &arial, black_ref, None),
        (PAYER_BANK_COORD, "Банк плательщика", 9.0, &arial, black_ref, None),
        (BIK2_COORD, "БИК", 9.0, &arial, black_ref, None),
        (ACCOUNT_NUMBER3_COORD, "Сч. №", 9.0, &arial, black_ref, None),
        (PAYEE_BANK_COORD, "Банк получателя", 9.0, &arial, black_ref, None),
        (INN2_COORD, "ИНН", 9.0, &arial, black_ref, None),
        (KPP2_COORD, "КПП", 9.0, &arial, black_ref, None),
        (ACCOUNT_NUMBER4_COORD, "Сч. №", 9.0, &arial, black_ref, None),
        (PAYMENT_TYPE_COORD, "Вид оп.", 9.0, &arial, black_ref, None),
        (PAYMENT_TERM_COORD, "Срок плат.", 9.0, &arial, black_ref, None),
        (PAYMENT_PURPOSE_COORD, "Наз. пл.", 9.0, &arial, black_ref, None),
        (PAYMENT_QUE_COORD, "Очер. плат.", 9.0, &arial, black_ref, None),
        (PAYMENT_CODE_COORD, "Код", 9.0, &arial, black_ref, None),
        (PAYMENT_RESERVE_COORD, "Рез. поле", 9.0, &arial, black_ref,  None),
        (PAYEE_COORD, "Получатель", 9.0, &arial, black_ref, None),
        (PAYMENT_PURPOSE_FULL_COORD, "Назначение платежа", 9.0, &arial, black_ref, None),
        (SIGN_COORD, "Подписи", 9.0, &arial, black_ref, None),
        (BANK_SIGNS_COORD, "Отметки банка", 9.0, &arial, black_ref, None),
        (PAID_COORD, "ОПЛАЧЕНО", 7.0, &arial, blue_ref, None),
        (STAMP_COORD, "М.П.", 9.0, &arial, black_ref, None),
    ];

    let payer_bank_with_city = format!("{} {}", payment_order.payer_bank, payment_order.payer_bank_address);
    let payee_bank_with_city = format!("{} {}", payment_order.side_recipient_bank, payment_order.side_recipient_bank_address);

    let side_recipient_kpp: String = match &payment_order.side_recipient_kpp {
        Some(kpp) => kpp.to_string(),
        None => String::from(""),
    };

    let literal_sum: String = match &payment_order.literal_sum {
        Some(sum) => sum.to_string(),
        None => String::from(""),
    };

    let status: String = match &payment_order.status {
        Some(status) => status.to_string(),
        None => String::from(""),
    };

    let purpose_code: String = match &payment_order.purpose_code {
        Some(purpose_code) => purpose_code.to_string(),
        None => String::from(""),
    };

    let uin: String = match &payment_order.uin {
        Some(uin) => uin.to_string(),
        None => String::from("0"),
    };

    let cbc: String = match &payment_order.cbc {
        Some(cbc) => cbc.to_string(),
        None => String::from(""),
    };

    let okato: String = match &payment_order.okato {
        Some(okato) => okato.to_string(),
        None => String::from(""),
    };

    let reason: String = match &payment_order.reason {
        Some(reason) => reason.to_string(),
        None => String::from(""),
    };

    let period: String = match &payment_order.period {
        Some(period) => period.to_string(),
        None => String::from(""),
    };

    let reason_number: String = match &payment_order.reason_number {
        Some(reason_number) => reason_number.to_string(),
        None => String::from(""),
    };

    let reason_date: String = match &payment_order.reason_date {
        Some(reason_date) => reason_date.to_string(),
        None => String::from(""),
    };

    let field_110: String = match &payment_order.field_110 {
        Some(field_110) => field_110.to_string(),
        None => String::from(""),
    };

    let data_texts: [((Mm, Mm), &str, f64, &IndirectFontRef, &Color,  Option<Mm>); 35] = [ 
        (DATA_INCOME_COORD, payment_order.creation_date.as_str(), 9.0, &arial, black_ref, None),
        (DATA_OUTCOME_COORD, payment_order.last_transaction_date.as_str(), 9.0, &arial, black_ref, None),
        (DATA_PAYMENT_ORDER_COORD, payment_order.document_number.as_str(), 9.0, &arial_bold, black_ref, None),
        (DATA_LITERAL_SUM_COORD, literal_sum.as_str(), 9.0, &arial, black_ref, Some(Mm(158.5))),
        (DATA_DATE_COORD, payment_order.document_date.as_str(), 9.0, &arial, black_ref, None),
        (DATA_INN1_COORD, payment_order.payer_inn.as_str(), 9.0, &arial, black_ref, None),
        (DATA_KPP1_COORD, payment_order.payer_kpp.as_str(), 9.0, &arial, black_ref, None),
        (DATA_SUM_COORD, payment_order.transaction_sum.as_str(), 9.0, &arial, black_ref, None),
        (DATA_PAYER_COORD, payment_order.payer_name.as_str(), 9.0, &arial, black_ref, Some(Mm(99.5))),
        (DATA_ACCOUNT_NUMBER1_COORD, payment_order.payer_account.as_str(), 9.0, &arial, black_ref, None),
        (DATA_PAYER_BANK_COORD, payer_bank_with_city.as_str(), 9.0, &arial, black_ref, Some(Mm(99.5))),
        (DATA_BIK1_COORD, payment_order.payer_bank_code.as_str(), 9.0, &arial, black_ref, None),
        (DATA_ACCOUNT_NUMBER2_COORD, payment_order.payer_cr_account.as_str(), 9.0, &arial, black_ref, None),
        (DATA_PAYEE_BANK_COORD, payee_bank_with_city.as_str(), 9.0, &arial, black_ref, Some(Mm(99.5))),
        (DATA_BIK2_COORD, payment_order.side_recipient_bank_code.as_str(), 9.0, &arial, black_ref, None),
        (DATA_ACCOUNT_NUMBER3_COORD, payment_order.side_recipient_cr_account.as_str(), 9.0, &arial, black_ref, None),
        (DATA_INN2_COORD, payment_order.side_recipient_inn.as_str(), 9.0, &arial, black_ref, None),
        (DATA_KPP2_COORD, side_recipient_kpp.as_str(), 9.0, &arial, black_ref, None),
        (DATA_ACCOUNT_NUMBER4_COORD, payment_order.side_recipient_account.as_str(), 9.0, &arial, black_ref, None),
        (DATA_PAYEE_COORD, payment_order.side_recipient_name.as_str(), 9.0, &arial, black_ref, Some(Mm(99.5))),
        (DATA_PAYMENT_CODE_COORD, payment_order.transaction_type_code.as_str(), 9.0, &arial, black_ref, None),
        (DATA_PAYMENT_QUE_COORD, payment_order.priority.as_str(), 9.0, &arial, black_ref, None),
        (DATA_FULL_PURPOSE_COORD, payment_order.purpose.as_str(), 9.0, &arial, black_ref, Some(Mm(180.1))),
        (DATA_PAID, payment_order.last_transaction_date.as_str(), 6.7, &arial, blue_ref, None),
        (HEAD_FULL_NAME_COORD, payment_order.finance_administrator_name.as_str(), 10.0, &arial, black_ref, None),
        (DATA_PURPOSE_CODE, purpose_code.as_str(), 9.0, &arial, black_ref, None),
        (DATA_UIN_CODE, uin.as_str(), 9.0, &arial, black_ref, None),
        (DATA_STATUS, status.as_str(), 9.0, &arial, black_ref, None),
        (DATA_CBC, cbc.as_str(), 9.0, &arial, black_ref, None),
        (DATA_OKATO, okato.as_str(), 9.0, &arial, black_ref, None),
        (DATA_REASON, reason.as_str(), 9.0, &arial, black_ref, None),
        (DATA_PERIOD, period.as_str(), 9.0, &arial, black_ref, None),
        (DATA_REASON_NUMBER, reason_number.as_str(), 9.0, &arial, black_ref, None),
        (DATA_REASON_DATE, reason_date.as_str(), 9.0, &arial, black_ref, None),
        (DATA_FIELD_110, field_110.as_str(), 9.0, &arial, black_ref, None),
    ];

    for &((coords_x, coords_y), length, color, line_type) in lines.iter() {
        add_line(&current_layer, (coords_x, coords_y), length, color, line_type)
    };

    for &((coords_a, coords_b, coords_c, coords_d), color,) in rectangles.iter() {
        add_rectangle(&current_layer, (coords_a, coords_b, coords_c, coords_d), color);
    };

    for &((coords_x, coords_y), text, size, font, color, field_width) in default_texts.iter() {
        write_text_to_pdf(&current_layer, (coords_x, coords_y), text, size, font, color, field_width);
    };

    for &((coords_x, coords_y), text, size, font, color, field_width) in data_texts.iter() {
        write_text_to_pdf(&current_layer, (coords_x, coords_y), text, size, font, color, field_width);
    };

    doc = doc.with_conformance(PdfConformance::Custom(CustomPdfConformance {
    	requires_icc_profile: false,
    	requires_xmp_metadata: false,
        .. Default::default()
    }));

    let bytes = doc.save_to_bytes();
    
    Ok(bytes.unwrap())
}
