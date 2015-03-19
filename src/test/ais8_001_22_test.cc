// Test parsing 8:1:22.

#include <memory>

#include "gtest/gtest.h"
#include "ais.h"
#include "ais8_001_22.h"

namespace libais {
namespace {

std::unique_ptr<Ais8_001_22> Init(const string &nmea_string) {
  const string body(GetBody(nmea_string));
  const int pad = GetPad(nmea_string);

  // TODO(schwehr): Switch to c++14 make_unique.
  std::unique_ptr<Ais8_001_22> msg(new Ais8_001_22(body.c_str(), pad));
  if (!msg || msg->had_error()) {
    return nullptr;
  }
  return msg;
}

void Validate(
    const Ais8_001_22 *msg,
    const int message_id,
    const int repeat_indicator,
    const int mmsi,
    const int link_id,
    const int notice_type,
    const int month,
    const int day,
    const int hour,
    const int minute,
    const int duration_minutes) {
  ASSERT_NE(nullptr, msg);
  ASSERT_EQ(message_id, msg->message_id);
  ASSERT_EQ(repeat_indicator, msg->repeat_indicator);
  ASSERT_EQ(mmsi, msg->mmsi);
  ASSERT_EQ(1, msg->dac);
  ASSERT_EQ(22, msg->fi);

  ASSERT_EQ(0, msg->spare);

  ASSERT_EQ(link_id, msg->link_id);
  ASSERT_EQ(notice_type, msg->notice_type);
  ASSERT_EQ(month, msg->month);
  ASSERT_EQ(day, msg->day);
  ASSERT_EQ(hour, msg->hour);
  ASSERT_EQ(minute, msg->minute);
  ASSERT_EQ(duration_minutes, msg->duration_minutes);
}

// Tests decoding a Boston right whale alert message.
TEST(Ais8_1_22Test, CircleAndTextForMarineMammals) {
  std::unique_ptr<Ais8_001_22> msg = Init(
      "!AIVDM,1,1,0,B,803Ovrh0EPM0WB0h2l0MwJUi=6B4G9000aip8<2Bt2H"
      "q2Qhp,0*01,d-084,S1582,t091042.00,T42.19038981,r003669945,"
      "1332321042");
  Validate(msg.get(), 8, 0, 3669739, 29, 1, 3, 20, 16, 6, 1440);

  ASSERT_EQ(2, msg->sub_areas.size());

  ASSERT_EQ(AIS8_001_22_SHAPE_CIRCLE, msg->sub_areas[0]->getType());
  ASSERT_EQ(AIS8_001_22_SHAPE_TEXT, msg->sub_areas[1]->getType());

  Ais8_001_22_Circle *circle =
      dynamic_cast<Ais8_001_22_Circle *>(msg->sub_areas[0]);

  ASSERT_FLOAT_EQ(-70.22429656982422, circle->x);
  ASSERT_FLOAT_EQ(42.105865478515625, circle->y);
  ASSERT_EQ(4, circle->precision);
  ASSERT_EQ(14810, circle->radius_m);
  ASSERT_EQ(0, circle->spare);

  Ais8_001_22_Text *text = dynamic_cast<Ais8_001_22_Text *>(msg->sub_areas[1]);

  ASSERT_STREQ("NOAA RW SGHTNG", text->text.c_str());
}

// Tests missing subareas.
TEST(Ais8_1_22Test, BadAreaNotice) {
  std::unique_ptr<Ais8_001_22> msg = Init(
      "!AIVDM,1,1,,A,803Ovrh0EPG0WB5p2l0L40,4*1E,d-085,S1593"
      ",t091042.00,T42.48370895,r003669945,1332321042");
  ASSERT_EQ(nullptr, msg);
}

// Tests missing subareas and incorrect pad.
TEST(Ais8_1_22Test, BadAreaNoticeAndWrongPad) {
  std::unique_ptr<Ais8_001_22> msg = Init(
      "!AIVDM,1,1,,A,803Ovrh0EPG0WB5p2l0L40,4*1E,d-085,S1593"
      ",t091042.00,T42.48370895,r003669945,1332321042");
  ASSERT_EQ(nullptr, msg);
}

}  // namespace
}  // namespace libais